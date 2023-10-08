# cubescramble-rewrite
Python based speedcubing (currenty only for clock) trainer software.

Created in python `3.10.4` 
with pygame `2.1.2` (`SDL 2.0.18`), sounddevice `0.4.6`, numpy `1.22.3` and requests `2.28.1`

## Setup
Install [pygame](https://pypi.org/project/pygame), [sounddevice](https://pypi.org/project/sounddevice), [numpy](https://pypi.org/project/numpy) and [requests](https://pypi.org/project/requests)

### `*nix` or `*bsd` or `MacOS`
```sh
pip3 install pygame sounddevice numpy requests
```
or if didn't work
```sh
pip install pygame sounddevice numpy requests
```

### Windows
```cmd
py -3 -m pip install pygame sounddevice numpy requests
```

## Run

### `*nix` or `*bsd` or `MacOS`
```sh
python3 main.py
```

If the programs gives error like this:
```
Traceback (most recent call last):
  File ".../cubescramble-rewrite/game.py", line ..., in <module>
    import sounddevice as sd
  File ".../site-packages/sounddevice.py", line ..., in <module>
    raise OSError('PortAudio library not found')
OSError: PortAudio library not found
```

try:
```sh
sudo apt-get install libportaudio2
```

or if that didn't work

```sh
sudo apt-get install libasound-dev
```

### Windows

```cmd
py -3 main.py
```

For help, feel free to open an issue!
