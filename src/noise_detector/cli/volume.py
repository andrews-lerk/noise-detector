import audioop
import logging

import pyaudio
from tqdm import tqdm

from noise_detector.infrastructure.logging import setup_logging
from noise_detector.common import Config


def main() -> None:
    setup_logging()
    config = Config.load_config()

    pa = pyaudio.PyAudio()

    logging.info("Initializing audio devices...")

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
    logging.info("Volume level RMS...")
    try:
        with tqdm(total=7000, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [RMS]') as volume_level:
            while True:
                data = stream.read(stream._frames_per_buffer, exception_on_overflow=False)
                rms = audioop.rms(data, 2)
                volume_level.update(rms)
                volume_level.refresh()
                volume_level.n = 0
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Stop received")
    finally:
        stream.close()
        stream.stop_stream()
        pa.terminate()
        logging.warning("Stopped stream, pyaudio terminated")


if __name__ == "__main__":
    main()
