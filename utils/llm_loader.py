from langchain_community.llms.llamacpp import LlamaCpp as Llama
import os

def load_llm():
    parent_dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(parent_dir_name, "models", "mistral-7b-v0.1.Q4_K_M.gguf")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please download the model first.")
    
    return Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=2,  # Adjust based on your CPU cores
        temperature=0.4,
        max_tokens=1024,
        verbose=True
    )
