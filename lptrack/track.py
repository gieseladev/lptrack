import dataclasses
from typing import Optional

__all__ = ["Track"]


# TODO source name

# TODO source manager details

@dataclasses.dataclass(unsafe_hash=True)
class Track:
    """Information contained in a track data message body.

    Implements a hash method, but isn't immutable. Be careful when hashing
    instances while still mutating them!

    Attributes:
        title (str): Title of the track
        author (str): Author of the track.
        duration (float): Duration of the track in seconds.
        identifier (str): Identifier of the track.
        is_stream (bool): Whether the track is a stream.

        uri (Optional[str]): URI of the track. Definitely `None`
            before `version` 2, optional for version 2 and up.
            The uri is ignored for equality tests.

        version (Optional[int]): Track version. If this isn't set, the
            latest version (supported by the library) is assumed.
            The version is ignored for equality tests.
    """

    title: str
    author: str
    duration: float
    identifier: str
    is_stream: bool
    uri: Optional[str] = dataclasses.field(default=None, compare=False)

    version: Optional[int] = dataclasses.field(default=None, compare=False)
