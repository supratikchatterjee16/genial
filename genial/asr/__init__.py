import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
from transformers.utils import logging

logging.get_logger("transformers").setLevel(logging.ERROR)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
sample = dataset[0]["audio"]

result = pipe(sample)
print(result["text"])

result = pipe("/home/supratik/Downloads/audio.wav")
print(result["text"])

result = pipe("/home/supratik/Downloads/sample1.flac")
print(result["text"])

# import torch
# import pyaudio
# import numpy as np

# from datasets import load_dataset
# from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# torch.cuda.empty_cache()
# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# model_id = "/home/supratik/Documents/datasets/whisper-tiny"

# model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
# model.to(device)

# processor = AutoProcessor.from_pretrained(model_id)

# pipe = pipeline(
#     "automatic-speech-recognition",
#     model=model,
#     tokenizer=processor.tokenizer,
#     feature_extractor=processor.feature_extractor,
#     max_new_tokens=128,
#     chunk_length_s=30,
#     batch_size=16,
#     return_timestamps=True,
#     torch_dtype=torch_dtype,
#     device=device,
# )

# dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
# sample = dataset[0]["audio"]
# # print(sample)
# # recognizer = sr.Recognizer()

# # with sr.Microphone(device_index=0) as source :
# #     print('Ready.')
# #     audio = recognizer.listen(source, timeout=None)
# #     wav_data = audio.get_raw_data()
# #     pre_process = torch.from_numpy(np.frombuffer(wav_data, np.int16).flatten().astype(np.float32) / 32768.0)
# #     result = pipe(pre_process.numpy())
# #     print(result["text"])

# p = pyaudio.PyAudio()
# duration = 5
# fs = 8000
# stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer= duration * fs)
# while True:
#     print("Ready")
#     buffer = stream.read(duration * fs)
#     array = np.frombuffer(buffer, dtype='int16').astype(np.float32) / 32767.0
#     # data = {'array' : torch.from_numpy(array).float().numpy(), 'sampling_rate' : fs}
#     data = {'array' : array, 'sampling_rate' : fs}
#     print(data)
#     result = pipe(data)
#     print(result["text"])