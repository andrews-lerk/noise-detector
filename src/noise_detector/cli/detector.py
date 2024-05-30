import logging

import pyaudio

from noise_detector.infrastructure.logging import setup_logging
from noise_detector.common import Config


def main() -> None:
    setup_logging()
    config = Config.load_config()
    logging.info("Loaded config")

    pa = pyaudio.PyAudio()
    for i in range(1, pa.get_device_count()):
        logging.info(pa.get_device_info_by_index(i))
    stream = pa.open(
        format=pyaudio.paInt16, channels=config.channels, rate=config.rate, input=True, frames_per_buffer=config.chunk,
    )


if __name__ == "__main__":
    main()
