import torch
import torchaudio
from torchaudio.transforms import Resample
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

processor = Wav2Vec2Processor.from_pretrained("ai4bharat/indicwav2vec-hindi")
model = Wav2Vec2ForCTC.from_pretrained("ai4bharat/indicwav2vec-hindi")


# Set audio backend
torchaudio.set_audio_backend("soundfile")

def transcribe_audio(file: str) -> str:
    waveform, sr = torchaudio.load(file)
    
    # Resample if the sample rate is not 16kHz
    if sr != 16000:
        resampler = Resample(orig_freq=sr, new_freq=16000)
        waveform = resampler(waveform)
        sr = 16000

    input_values = processor(waveform[0], sampling_rate=sr, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    return transcription

