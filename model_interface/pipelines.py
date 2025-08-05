from model_interface.llms import (
    Llama_3p1_8B_Instruct_4BitQuantized, ModelStatus, LargeLanguageModel
)
from model_interface.prompts import Prompt
from typing import Generator, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., object])

class BasicReflexivePipeline:
    def __init__(self):
        self.__model: LargeLanguageModel = Llama_3p1_8B_Instruct_4BitQuantized()

        if self.__model.load() != ModelStatus.READY:
            print("Failed to load model before timeout.")
            self.__model.unload()
            raise RuntimeError("Unable to load model before timeout.")
        
        self.__prompt_maker = Prompt()
        self.__callback: Callable[[str], None] | None = None
        self.__model_tool_docs: str = self.__model.get_tool_integrator().get_tool_prompt()

    def register_callback(self) -> Callable[[Callable[[str], None]], Callable[[str], None]]:
        def decorator(func: Callable[[str], None]) -> Callable[[str], None]:
            self.__callback = func
            return func
        return decorator
    
    def inject_stream(self, prompts: list[str], debug: bool=True) -> None:
        if not self.__callback:
            raise RuntimeError("Callback function not provided")

        # Prepare prompts
        final_prompts: list[str] = [
            self.__prompt_maker.get_cot_conv_prompt(
                query=prompt, use_cached=False, tools=self.__model_tool_docs
            )
            for prompt in prompts
        ]

        # Step - 1 : Initial Responses
        step1_responses: list[str] = self.__model.call(final_prompts)

        # Step - 2 : Reflect on the Responses
        REFLECTION_PROMPT_ROOT = "Based on the original query and the original response, refine the response so that it answers the user query accurately. Original Query: "

        step2_prompts: list[str] = [
            REFLECTION_PROMPT_ROOT + prompts[i] +
            " Original Response: " + step1_responses[i] + "Refined Response: "
            for i in range(0, len(prompts))
        ]

        for token in self.__model.call_stream(step2_prompts):
            self.__callback(token)

    def __del__(self):
        self.__model.unload()

def main():
    pipeline = BasicReflexivePipeline()

    @pipeline.register_callback()
    def callback(token: str) -> None:
        print(token, flush=True, end='')

    pipeline.inject_stream(["What's the weather in New Delhi"])

if __name__ == "__main__":
    main()