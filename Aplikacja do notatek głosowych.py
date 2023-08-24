import tkinter as tk
import pyaudio
import wave

class VoiceNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja do notatek głosowych")

        self.record_button = tk.Button(root, text="Nagrywaj", command=self.start_recording)
        self.record_button.pack()

        self.stop_button = tk.Button(root, text="Zatrzymaj", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.play_button = tk.Button(root, text="Odtwórz", command=self.play_recording, state=tk.DISABLED)
        self.play_button.pack()

        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, frames_per_buffer=1024, input=True)
        self.is_recording = True
        self.frames = []
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)

    def play_recording(self):
        if self.frames:
            wf = wave.open("recording.wav", "wb")
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b"".join(self.frames))
            wf.close()

            self.frames = []

            wf = wave.open("recording.wav", "rb")
            stream = self.audio.open(format=self.audio.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
            data = wf.readframes(1024)
            while data:
                stream.write(data)
                data = wf.readframes(1024)
            stream.stop_stream()
            stream.close()

    def callback(self, in_data, frame_count, time_info, status):
        if self.is_recording:
            self.frames.append(in_data)
        return in_data, pyaudio.paContinue

    def run(self):
        self.audio_stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, frames_per_buffer=1024, stream_callback=self.callback, input=True)
        self.root.mainloop()
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio.terminate()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceNoteApp(root)
    app.run()
s
