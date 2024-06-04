import pyaudio
from pyaudio import Stream


class Detector:
    def __init__(self, stream: Stream, listen_time: int) -> None:

        self.stream = stream
        self.listen_time = listen_time

        self._audio_data_buff = []

    def start_listening(self) -> None:
        for i in range(self.stream._rate / self.stream._frames_per_buffer * self.listen_time):
            string_audio_data = self.stream.read(self.stream._frames_per_buffer, exception_on_overflow=False)
