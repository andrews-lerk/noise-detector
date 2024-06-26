import argparse
import logging
import time
import datetime
from pathlib import Path

import pyaudio

from noise_detector.infrastructure.logging import setup_logging
from noise_detector.common import Config
from noise_detector.application import Detector


def main(argv: argparse.Namespace) -> None:
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
    if argv.delay > 0:
        logging.warning(
            "Delay detector start until: %s",
            (datetime.datetime.now() + datetime.timedelta(seconds=argv.delay)).strftime("%Y-%m-%d %H:%M:%S")
        )
        time.sleep(argv.delay)

    stream = pa.open(
        format=pyaudio.paInt16,
        channels=config.channels,
        rate=config.rate,
        input=True,
        frames_per_buffer=config.chunk,
        input_device_index=input_device
    )

    detector = Detector(
        stream, argv.listen_secs, config.rms_detection_value, Path(__file__).parent.parent.parent.parent / "results"
    )

    try:
        detector.start_listening()
    except (KeyboardInterrupt, SystemExit):
        logging.error("Stop received")
    finally:
        stream.close()
        stream.stop_stream()
        pa.terminate()
        logging.warning("Stopped stream, pyaudio terminated")

    logging.info("Detector finished")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Noise detector')
    parser.add_argument("-ls", "--listen_secs", type=int, default=0, help='Listen time in secs')
    parser.add_argument("-d", "--delay", type=int, default=0, help='Delay detector start in seconds')
    main(parser.parse_args())
