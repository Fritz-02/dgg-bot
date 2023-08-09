import dataclasses
from typing import Union

import requests


@dataclasses.dataclass
class Flair:
    label: str
    name: str
    description: str
    hidden: bool
    priority: int
    color: str
    rainbowColor: bool
    image: list[dict]

    def __repr__(self):
        return f"Flair<{self.label}>"

    def __hash__(self):
        return hash(self.name)


def flair_converter(endpoint: str) -> dict:
    """Returns a dict to convert flair names (e.g. flair17) to a Flair object."""
    r = requests.get(endpoint)
    converter = {item["name"]: Flair(**item) for item in r.json()}
    return converter


def convert_flairs(flair_dict: dict, features: list = None) -> Union[list[Flair], None]:
    """Converts a list of features into their corresponding Flairs, using a dict created from flair_converter."""
    if features:
        return [flair_dict[flair] for flair in features]
