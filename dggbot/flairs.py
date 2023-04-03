import dataclasses
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


def flair_converter(endpoint: str) -> dict:
    """Returns a dict to convert flair names (e.g. flair17) to a Flair object."""
    r = requests.get(endpoint)
    converter = {item["name"]: Flair(**item) for item in r.json()}
    return converter
