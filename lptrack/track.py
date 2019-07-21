import dataclasses
from typing import Optional

__all__ = ["Track"]


@dataclasses.dataclass()
class Track:
    title: str
    author: str
    duration: float
    identifier: str
    is_stream: bool
    uri: Optional[str]

    version: Optional[int] = None
