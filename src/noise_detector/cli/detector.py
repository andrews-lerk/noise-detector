import logging

import pyaudio

from noise_detector.infrastructure.logging import setup_logging
from noise_detector.common import Config


def main() -> None:
    setup_logging()
    config = Config.load_config()
    logging.info("Loaded config")

    pa = pyaudio.PyAudio()
    devices = [pa.get_device_info_by_index(i) for i in range(1, pa.get_device_count())]
    input_device = int(input(
        "\nChoose input device:\n" + "".join(list(
            f"{i['index']}. "
            f"\'{i['name']}\' with input channels: "
            f"{i['maxInputChannels']}, "
            f"sample rate: {i['defaultSampleRate']}\n" for i in devices
        )
        ) +
        "Enter number of input device: "
    )
    )
    logging.info("Input device selected with index: %s", input_device)
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=config.channels,
        rate=config.rate,
        input=True,
        frames_per_buffer=config.chunk,
        input_device_index=input_device
    )
    logging.info("Stream is opened")


if __name__ == "__main__":
    main()
