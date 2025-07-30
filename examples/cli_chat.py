from model_interface import prompts, llms

LLM = llms.Llama_3p1_8B_Instruct_4BitQuantized()
PROMPT_MAKER = prompts.Prompt()
TOOL_DOCS = LLM.get_tool_integrator().get_tool_prompt()

# Loading LLM
if LLM.load() != llms.ModelStatus.READY:
    print("Failed to load model before timeout.")
    LLM.unload()
    raise RuntimeError("LLM loading failed.")

def cli_chat_driver(query: str):
    prompt = PROMPT_MAKER.get_cot_conv_prompt(
        query=query, use_cached=False
    )

    for token in LLM.call_stream([prompt], reflection=True):
        print(token, end='', flush=True)

def main():
    while True:
        query = str(input("User> "))

        if query == 'q':
            LLM.unload()
            break
        else:
            cli_chat_driver(query)

if __name__ == "__main__":
    main()
