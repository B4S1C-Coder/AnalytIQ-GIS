from llama_cpp import Llama

meta_llama_3p1_8b_it_q4_k_m = Llama(
    model_path='../models/llama-3.1-8b-it-q4-k-m/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf',
    n_gpu_layers=20, n_ctx=4096, use_mlock=True, use_mmap=True, verbose=True
)

prompt = "<s>[INST] What is the difference between IPv4 and IPv6? [/INST]"
output = meta_llama_3p1_8b_it_q4_k_m(prompt, max_tokens=256, echo=True)

print(output["choices"][0]["text"])
