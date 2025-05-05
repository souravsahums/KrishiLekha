from huggingface_hub import hf_hub_download
import os

def download_model():
    # Download the model from Hugging Face Hub
    # TheBloke/Mistral-7B-v0.1-GGUF is a placeholder; replace with the actual model repo ID
    # "mistral-7b-v0.1.Q4_K_M.gguf" is a placeholder; replace with the actual filename if different
    # "models" is the local directory where the model will be saved
    
    # Ensure the local directory exists
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(parent_dir, "models")
    # check if the model file already exists
    model_file_path = os.path.join(model_dir, "mistral-7b-v0.1.Q4_K_M.gguf")
    
    if os.path.exists(model_file_path):
        print(f"Model file already exists at {model_file_path}.")
        return model_file_path
    else:
        os.makedirs(model_dir, exist_ok=True)

    # Download the model file
    model_path = hf_hub_download(
        repo_id="TheBloke/Mistral-7B-v0.1-GGUF",
        filename="mistral-7b-v0.1.Q4_K_M.gguf",
        local_dir=f"{model_dir}"
    )

    print(f"Model downloaded and saved to {model_path}.")
    return model_path

if __name__ == "__main__":
    download_model()
