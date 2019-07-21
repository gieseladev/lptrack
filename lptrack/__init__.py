import base64
import io
from typing import Union

# needs to come after track import
from .format import *
from .track import *


def decode(data: Union[str, bytes]) -> Track:
    decoded = base64.b64decode(data)
    return Decoder(io.BytesIO(decoded)).decode()


def encode(track: Track) -> bytes:
    buf = io.BytesIO()
    Encoder(buf).encode(track)
    return base64.b64encode(buf.getvalue())
