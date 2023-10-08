import json
from dataclasses import dataclass, field
from typing import List

CONFIG_FILE = 'config.json'


@dataclass
class Config:
    device_num: int
    background_url: str
    background_local: bool
    background_scale: str
    times: List[int] = field(default_factory=list)
    particles: bool = True
    hide_mouse: bool = True

    def load(self):
        with open('config.json', 'r') as file:
            raw = json.load(file)
        for i in raw:
            item = self._load(raw[i], self.__annotations__[i])
            exec(f'self.{i} = item')

    def _load(self, raw, t):
        if type(raw) == int:
            return int(raw)
        elif type(raw) == str:
            return str(raw)
        elif type(raw) == bool:
            return bool(raw)
        elif type(raw) == list:
            out = []
            for item in raw:
                out.append(self._load(item, None))
            return out
        # TODO: tuples

        out = t()
        out.load(raw)
        return out
        # exec(f'self.{i} = {t}().load({raw[i]})')

    def save(self):
        out = {}
        for i in self.__annotations__:
            out[i] = self._save(eval(f'self.{i}'))
        with open(CONFIG_FILE, 'w') as file:
            json.dump(out, file)

    def _save(self, raw):
        if type(raw) == int:
            return raw
        elif type(raw) == str:
            return raw
        elif type(raw) == bool:
            return raw
        elif type(raw) == list:
            out = []
            for item in raw:
                out.append(self._save(item))
            return out

        return raw.save()