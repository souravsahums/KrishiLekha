from llama_cpp import Llama

def load_llm(model_path):
    return Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=4,  # Adjust based on your CPU cores
        temperature=0.1,
        max_tokens=1024,
        verbose=True
    )
