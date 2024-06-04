# noise-detector
### Simple program to detect noise in the room

The main parameter for noise detection is RMS (https://en.wikipedia.org/wiki/Root_mean_square), 
in the current version of the program you need to manually set the optimal RMS parameter, 
to do this run `make volume`, details below

### Installation
1. Install pdm (https://pdm-project.org/en/latest/)
2. Clone repository 
```shell
git clone https://github.com/andrews-lerk/noise-detector.git
```
3. Create env and install depends
```shell
make install && make init
```
### Configuration
Optimal configuration (set manually - `rms_detection_value` parameter):
```yaml
rate: 30000 
chunk: 1024
channels: 1
rms_detection_value: 7000 # manually set the optimal RMS parameter
```

### Usage
Run detector:

**listen_secs** - listen seconds of detector working **after delay**

**delay** - sleeping time before detector listening start

**Results sound records will be locale in the `results` directory**
```shell
make detector listen_secs=28800 delay=3600
```

Present volume level:
```shell
make volume
```
Using the displayed scale, you can manually identify the approximate RMS value at which recording begins