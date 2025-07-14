from abc import ABC, abstractmethod
from enum import Enum
from multiprocessing import Process, Pipe
from multiprocessing.connection import PipeConnection
import traceback
from typing import Any

class ModelStatus(Enum):
    READY  = 1  # Model is ready for use
    LOAD   = 2  # Model is being loading for use
    UNLOAD = 3  # Model is being unloaded or unloaded
    INJEST = 4  # Model is injesting messages from queue
    EJECT  = 5  # Model is writing responses to queue
    ERROR  = 6  # Model has encountered an unrecoverable error

# This call will represent and handle interactions with LLMs (or LLM APIs) outside the model_interface package
class LargeLanguageModel(ABC):
    """ Base class that manages dedicated process for the LLM. """
    def __init__(self):
        self.__status = ModelStatus.UNLOAD
        self.__process: Process | None = None
        self.__conn: PipeConnection | None = None # IPC Pipe Connection object
        self.__error: str | None = None

    def get_status(self) -> ModelStatus:
        return self.__status

    def get_error(self) -> str | None:
        return self.__error

    def load(self) -> ModelStatus:
        if self.__status in (ModelStatus.LOAD, ModelStatus.READY):
            return self.__status

        parent_conn, child_conn = Pipe()
        self.__conn = parent_conn

        self.__status = ModelStatus.LOAD
        self.__process = Process(target=self.__run_model_process, args=(child_conn,))
        self.__process.start()

        if parent_conn.poll(timeout=10):
            msg = parent_conn.recv()

            if msg[0] == "status" and msg[1] == "ready":
                self.__status = ModelStatus.READY
            elif msg[0] == "status" and msg[1] == "error":
                self.__status = ModelStatus.ERROR
                self.__error = msg[2]
        else:
            self.__status = ModelStatus.ERROR
            self.__error = "Timeout while loading model"

        return self.__status

    def __run_model_process(self, conn: PipeConnection):
        """ Runs in a separate process and handles model logic """
        try:
            model = self.__load_model()
            conn.send(("status", "ready"))
        except Exception:
            conn.send(("status", "error", traceback.format_exc()))
            return

        while True:
            msg = conn.recv()
            
            if msg == "terminate":
                break
            elif isinstance(msg, dict) and "prompts" in msg:
                try:
                    responses = [ model(prompt) for prompt in msg["prompts"] ]
                    conn.send(("result", responses))
                except Exception:
                    conn.send(("error", traceback.format_exc()))

    def unload(self):
        if self.__conn:
            try:
                self.__conn.send("terminate")
            except Exception:
                pass
        
        if self.__process:
            self.__process.join(timeout=5)

        self.__status = ModelStatus.UNLOAD
        self.__conn = None
        self.__process = None

    def call(self, prompts: list[str]) -> list[str]:
        if self.__status != ModelStatus.READY:
            raise RuntimeError(f"Model not ready. Status: {self.__status}")

        self.__status = ModelStatus.INJEST

        if not self.__conn:
            raise RuntimeError(f"Unable to communicate with model process. __conn is None.")

        self.__conn.send({"prompts": prompts})

        while True:
            if not self.__process or not self.__process.is_alive():
                self.__status = ModelStatus.ERROR
                self.__error = "Model process died unexpectedly."
                raise RuntimeError("Model process crashed unexpectedly")

            if self.__conn.poll(timeout=30):
                msg = self.__conn.recv()
                
                if msg[0] == "result":
                    self.__status = ModelStatus.EJECT
                    return msg[1]
                
                elif msg[0] == "error":
                    self.__status = ModelStatus.ERROR
                    self.__error = msg[1]
                    raise RuntimeError("Model error: " + msg[1])

    @abstractmethod
    def __load_model(self) -> Any:
        """ Derived classes must implement the loading logic and return the loaded model """
        pass

# This is a work in progress, and would be worked upon if the need for external APIs becomes necessary
class LargeLanguageModelAPI(LargeLanguageModel, ABC):
    """ This is a helper Base class to represent interactions with external LLM APIs as LargeLanguageModel instance. """
    def __init__(self):
        super().__init__()
        pass

    @abstractmethod
    def call(self, prompts: list[str]) -> list[str]:
        pass

    def __load_model(self) -> Any:
        return None