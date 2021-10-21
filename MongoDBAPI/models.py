from dataclasses import dataclass, field
from typing import List
import json


@dataclass
class TgUser:
    id: int = 0
    development: bool = False
    testing: bool = False
    administration: bool = False
    design: bool = False
    content: bool = False
    marketing: bool = False
    various: bool = False

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, ensure_ascii=False, indent=4)