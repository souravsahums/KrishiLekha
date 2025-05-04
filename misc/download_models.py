from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="TheBloke/Mistral-7B-v0.1-GGUF",
    filename="mistral-7b-v0.1.Q4_K_M.gguf",
    local_dir="models"
)
