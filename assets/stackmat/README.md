# stackmat-python
python based stackmat timer module

by coder13

# setup
install [https://pypi.org/project/sounddevice/](sounddevice)
## `*nix` or `*bsd` or `macos`
```sh
pip3 install sounddevice numpy
```
## windows
```cmd
py -3 -m pip install sounddevice numpy
```

in python
```python3
import sounddevice as sd
print(sd.query_devices())
```

you should see something like

```
  0 HDA Intel HDMI: Generic Digital (hw:0,3), ALSA (0 in, 2 out)
  1 HDA Intel PCH: ALC3235 Analog (hw:1,0), ALSA (2 in, 0 out)
  2 USB Audio Device: - (hw:2,0), ALSA (1 in, 2 out)
  3 hdmi, ALSA (0 in, 2 out)
  4 pulse, ALSA (32 in, 32 out)
* 5 default, ALSA (32 in, 32 out)
```

choose the device your stackmat is connected to. \
In `stackmat.py`, change the line
```python3
DEVICE_NUM = 8
```
to the number of the device you chose

