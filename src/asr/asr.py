import gradio as gr
from transformers import pipeline
import numpy as np


def transcribe(audio):
    sr, y = audio
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    return transcriber({"sampling_rate": sr, "raw": y})["text"]


transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")

demo = gr.Interface(
    transcribe,
    gr.Audio(),
    "text",
)

demo.launch()
print("ASR:__init__")