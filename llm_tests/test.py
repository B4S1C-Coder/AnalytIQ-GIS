from llama_cpp import Llama

llm = Llama(model_path="../models/phi2/phi-2.Q4_K_M.gguf", n_gpu_layers=20)
#output = llm("Q: What is the capital of France?\nA:", max_tokens=32)
#print(output["choices"][0]["text"])

def get_response(prompt: str) -> str:
    output = llm(f"Instruct: {prompt}\nOutput:", max_tokens=1024)
    return output["choices"][0]["text"]

while True:
    user_input = str(input("User> "))

    if user_input == "q":
        break

    print(get_response(user_input))
