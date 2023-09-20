import json
from dataclasses import dataclass

CONFIG_FILE = 'config.json'


@dataclass
class Config:
    device_num: int

    def load(self):
        with open('config.json', 'r') as file:
            raw = json.load(file)
        for i in raw:
            exec(f'self.{i} = {raw[i]}')

    def save(self):
        out = {}
        for i in self.__annotations__:
            out[i] = eval('self.' + i)
        with open(CONFIG_FILE, 'w') as file:
            json.dump(out, file)


if __name__ == '__main__':
    print(Config.__annotations__)
    c = Config(69)
    c.save()
    print(c.load())
