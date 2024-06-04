import datetime
import logging
import wave
from collections import deque
import audioop
from pathlib import Path

import pyaudio
from pyaudio import Stream


class Detector:
    def __init__(
            self,
            stream: Stream,
            listen_secs: int,
            rms_detection_value: int,
            output_dir: Path
    ) -> None:

        self.stream = stream
        self.listen_secs = listen_secs
        self.rms_detection_value = rms_detection_value
        self.output_dir = output_dir

        # stream data count per second
        self._data_count_per_sec = int(self.stream._rate / self.stream._frames_per_buffer)
        self._recording_state = False

        self._file = None

        # runtime buffers with fix length realized by two-way queues
        # buff maxlen = 2 seconds of recording for audio data and 3 seconds for sound level in the room
        self._audio_data_buff = deque(maxlen=self._data_count_per_sec * 1)
        self._rms_buff = deque(maxlen=self._data_count_per_sec * 3)

    def start_listening(self) -> None:
        logging.info("Starting listening...")
        for i in range(self._data_count_per_sec * self.listen_secs):
            self._read_stream()
            detection = self._analyze()
            if detection:
                if not self._recording_state:
                    logging.warning("Noise detected!")
                    logging.info("Start recording...")
                    self._recording_state = True
                    self._prepare_file()
                self._save_audio()
                continue

            if self._recording_state:
                logging.info("Stop recording, saved to file")
                self._file.close()
                self._recording_state = False
        logging.info("Listening finished")

    def _prepare_file(self) -> None:
        self._file = wave.open(
            str(self.output_dir) + f"/{datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')}.wav", 'wb'
        )
        self._file.setnchannels(self.stream._channels)
        self._file.setsampwidth(self.stream._parent.get_sample_size(pyaudio.paInt16))
        self._file.setframerate(self.stream._rate)

    def _read_stream(self) -> None:
        # read the data
        string_audio_data = self.stream.read(self.stream._frames_per_buffer, exception_on_overflow=False)
        rms = audioop.rms(string_audio_data, 2)
        # save buffers
        self._audio_data_buff.append(string_audio_data)
        self._rms_buff.append(rms)

    def _save_audio(self) -> None:
        self._file.writeframes(b''.join(self._audio_data_buff))
        self._audio_data_buff.clear()

    def _analyze(self) -> bool:
        return max(self._rms_buff) >= self.rms_detection_value
