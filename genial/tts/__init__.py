import os
import wave
import torch
import appdirs
import pyaudio
import soundfile as sf

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset

class TTSAgent:
    def __init__(self):
        # Load Model classes from model data
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

        # load xvector containing speaker's voice characteristics from a dataset
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    def _play_file(self, filename : str):
        # Load sound for listening to it
        file = wave.open(filename)
        player = pyaudio.PyAudio()
        stream = player.open(format = player.get_format_from_width(file.getsampwidth()),  
                    channels = file.getnchannels(),  
                    rate = file.getframerate(),  
                    output = True)  
        data = file.readframes(1024)
        while data:
            stream.write(data)
            data = file.readframes(1024)
        stream.stop_stream()  
        stream.close()
        player.terminate()

    def speak(self, text : str, should_speak : bool = True):
        # Process speech from inputs
        inputs = self.processor(text=text, return_tensors="pt")
        speech = self.model.generate_speech(inputs["input_ids"], self.speaker_embeddings, vocoder=self.vocoder)
        
        # Write out sound
        sf.write("speech.wav", speech.numpy(), samplerate=16000)

        if should_speak:
            self._play_file("speech.wav")
        
        os.remove('speech.wav')

def serve_tts():
    agent = TTSAgent()
    while True :
        agent.speak(input("User : "))

if __name__ == "__main__":
    serve_tts()