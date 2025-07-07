#include "llama.h"
#include <iostream>
#include <string>

int main(int argc, char **argv) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <model.gguf> <n_gpu_layers> <prompt>" << std::endl;
        return 1;
    }

    const std::string model_path   = argv[1];
    const int n_gpu_layers         = std::stoi(argv[2]);
    const std::string prompt_text = argv[3];

    // Initialize llama.cpp
    llama_backend_init();

    // Setup model params
    llama_model_params model_params = llama_model_default_params();
    model_params.n_gpu_layers = n_gpu_layers;

    // Load model
    llama_model *model = llama_load_model_from_file(model_path.c_str(), model_params);
    if (!model) {
        std::cerr << "Failed to load model!" << std::endl;
        return 1;
    }

    // Setup context
    llama_context_params ctx_params = llama_context_default_params();
    ctx_params.n_threads = 8; // Change this based on your CPU

    llama_context *ctx = llama_new_context_with_model(model, ctx_params);
    if (!ctx) {
        std::cerr << "Failed to create context!" << std::endl;
        return 1;
    }

    // Tokenize the prompt
    std::vector<llama_token> tokens(prompt_text.size() + 32);
    int n_tokens = llama_tokenize(model, prompt_text.c_str(), tokens.data(), tokens.size(), true);
    tokens.resize(n_tokens);

    // Evaluate the prompt
    if (llama_eval(ctx, tokens.data(), tokens.size(), 0, ctx_params.n_threads)) {
        std::cerr << "Evaluation failed!" << std::endl;
        return 1;
    }

    std::cout << "Prompt: " << prompt_text << std::endl;
    std::cout << "Response: ";

    // Generate 64 tokens
    llama_token last_token = 0;
    for (int i = 0; i < 64; ++i) {
        llama_token token = llama_sample_token_greedy(ctx);
        std::cout << llama_token_to_str(model, token);
        std::cout.flush();

        last_token = token;
        if (llama_eval(ctx, &token, 1, tokens.size() + i, ctx_params.n_threads)) {
            std::cerr << "\nGeneration failed!" << std::endl;
            break;
        }
    }

    std::cout << std::endl;

    // Cleanup
    llama_free(ctx);
    llama_free_model(model);
    llama_backend_free();
    return 0;
}

