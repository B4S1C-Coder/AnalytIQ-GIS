from abc import ABC, abstractmethod
from enum import Enum
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
import traceback
from typing import Any, cast
from llama_cpp import Llama
import os

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
        self.__conn: Connection | None = None # IPC Pipe Connection object
        self.__error: str | None = None

    def get_status(self) -> ModelStatus:
        return self.__status

    def get_error(self) -> str | None:
        return self.__error

    def load(self, timeout=30) -> ModelStatus:
        if self.__status in (ModelStatus.LOAD, ModelStatus.READY):
            return self.__status
        
        parent_conn, child_conn = Pipe()
        self.__conn = parent_conn

        self.__status = ModelStatus.LOAD
        self.__process = Process(target=self.__run_model_process, args=(child_conn,))
        self.__process.start()

        if parent_conn.poll(timeout=timeout):
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

    def __run_model_process(self, conn: Connection):
        """ Runs in a separate process and handles model logic """
        try:
            model = self._load_model()
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
                    msg_prompts = msg["prompts"]
                    kwargs = { k:v for k,v in msg.items() if k != "prompts" }
                    responses = self._handle_model_call(model, msg_prompts, **kwargs)
                    conn.send(("result", responses))
                except Exception:
                    conn.send(("error", traceback.format_exc()))

    @abstractmethod
    def _handle_model_call(self, model: Any, prompts: list[str], **kwargs) -> list[str]:
        pass

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

    def call(self, prompts: list[str], **kwargs) -> list[str]:
        if self.__status != ModelStatus.READY:
            raise RuntimeError(f"Model not ready. Status: {self.__status}")

        self.__status = ModelStatus.INJEST

        if not self.__conn:
            raise RuntimeError(f"Unable to communicate with model process. __conn is None.")

        self.__conn.send({"prompts": prompts, **kwargs})

        while True:
            if not self.__process or not self.__process.is_alive():
                self.__status = ModelStatus.ERROR
                self.__error = "Model process died unexpectedly."
                raise RuntimeError("Model process crashed unexpectedly")

            if self.__conn.poll(timeout=30):
                msg = self.__conn.recv()
                
                if msg[0] == "result":
                    # For now, NOT USING eject
                    self.__status = ModelStatus.READY
                    return msg[1]
                
                elif msg[0] == "error":
                    self.__status = ModelStatus.ERROR
                    self.__error = msg[1]
                    raise RuntimeError("Model error: " + msg[1])

    @abstractmethod
    def _load_model(self) -> Any:
        """ Derived classes must implement the loading logic and return the loaded model """
        pass

class Llama_3p1_8B_Instruct_4BitQuantized(LargeLanguageModel):
    def _load_model(self) -> Llama:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # Set logits_all=True to ue logprobs
        return Llama(
            model_path=os.path.join(
                base_dir, "models", "llama-3.1-8b-it-q4-k-m", "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
            ),
            n_gpu_layers=20, n_ctx=4096, use_mlock=True, use_mmap=True, verbose=True
        )
    
    def _handle_model_call(self, model: Llama, prompts: list[str], reflection: bool=False) -> list[str]:

        if reflection:
            return self.__reflection_handle_model_call(model, prompts)

        results: list[str] = []

        for prompt in prompts:
            response = cast(dict, model(
                prompt, max_tokens=256, echo=False, stream=False, temperature=0.7, top_k=50, top_p=0.9,
                repeat_penalty=1.1, stop=["</s>", "[/INST]", "User:", "Query:"]
            ))
            text = response["choices"][0]["text"].strip()
            results.append(text)

        return results

    def __reflection_handle_model_call(self, model: Llama, prompts: list[str]) -> list[str]:
        results: list[str] = []

        for prompt in prompts:
            # Step - 1: Generate Initial Response
            print("[ Initiated Step - 1 ]")

            # tokens = model.tokenize(prompt.encode('utf-8'), add_bos=True)
            # prompt_len = len(tokens)

            step1 = cast(dict, model(
                prompt, max_tokens=256, echo=True, stream=False, temperature=0.7, top_k=50, top_p=0.9,
                repeat_penalty=1.1, stop=["</s>", "[/INST]", "User:", "Query:"]
            ))

            # all_tokens = step1["tokens"]
            # output_tokens = all_tokens[prompt_len:]
            # logprobs = [t["logprob"] for t in output_tokens if "logprob" in t]
            step1_text = step1["choices"][0]["text"].strip()
            # confidence = sum(logprobs) / len(logprobs) if logprobs else -10.0

            # print(f"[ INITIAL CONFIDENCE: {confidence:.3f} ]")

            # Step - 2: Based on Initial Response, generate Final Response
            print("[ Initiated Step - 2 ]")

            reflection_prompt = f"""
            <s>[INST]
            You are a helpful assistant. Reflect on the previous response and improve it based on clarity, completeness and reasoning.
            User Query: {prompt.strip()}
            Initial Response: 
            {step1_text}

            Refined Answer:
            [/INST]
            """.strip()

            step2 = cast(dict, model(
                reflection_prompt, max_tokens=256, echo=False, stream=False, temperature=0.7, top_k=50, top_p=0.9,
                repeat_penalty=1.1, stop=["</s>", "[/INST]", "User:", "Query:"]
            ))

            final_output = step2["choices"][0]["text"].strip()
            results.append(final_output)

        return results

# This is a work in progress, and would be worked upon if the need for external APIs becomes necessary
class LargeLanguageModelAPI(LargeLanguageModel, ABC):
    """ This is a helper Base class to represent interactions with external LLM APIs as LargeLanguageModel instance. """
    def __init__(self):
        super().__init__()
        pass

    @abstractmethod
    def call(self, prompts: list[str]) -> list[str]:
        pass

    def _load_model(self) -> Any:
        return None

    def _handle_model_call(self, model: Any, prompts: list[str]) -> list[str]:
        return [""]