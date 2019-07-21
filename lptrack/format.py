import dataclasses
import enum
import io
from typing import Union

from . import Track, codec, versions

__all__ = ["Flags", "Header", "Decoder", "Encoder"]


class Flags(enum.IntFlag):
    TRACK_INFO_VERSIONED = 1


@dataclasses.dataclass()
class Header:
    flags: Flags
    size: int

    @property
    def is_versioned(self) -> bool:
        return (self.flags & Flags.TRACK_INFO_VERSIONED) > 0


class Decoder:
    _stream: codec.Reader

    def __init__(self, stream: Union[io.IOBase, codec.Reader]) -> None:
        if not isinstance(stream, codec.Reader):
            stream = codec.Reader(stream)

        self._stream = stream

    def read_header(self) -> Header:
        value = self._stream.read_int()
        flags = Flags((value & 0xC0000000) >> 30)
        size = value & 0x3FFFFFFF

        return Header(flags, size)

    def read_version(self) -> int:
        return self._stream.read_byte()

    def get_version(self, header: Header) -> int:
        if header.is_versioned:
            return self.read_version()
        else:
            return 1

    def read_body(self, version: int) -> Track:
        reader = versions.get_reader(version)
        return reader(self._stream)

    def decode(self) -> Track:
        header = self.read_header()
        version = self.get_version(header)
        return self.read_body(version)


class Encoder:
    _stream: codec.Writer

    def __init__(self, stream: Union[io.IOBase, codec.Writer]) -> None:
        if not isinstance(stream, codec.Writer):
            stream = codec.Writer(stream)

        self._stream = stream

    def write_header(self, header: Header) -> None:
        value = header.size | (header.flags << 30)
        self._stream.write_int(value)

    def encode(self, track: Track) -> None:
        body_buf = io.BytesIO()
        body_stream = codec.Writer(body_buf)

        version = track.version
        if version is None:
            version = versions.LATEST_VERSION

        flags = Flags(0)

        if version > 1:
            flags |= Flags.TRACK_INFO_VERSIONED
            body_stream.write_byte(version)

        writer = versions.get_writer(version)
        writer(body_stream, track)

        body_data = body_buf.getvalue()
        self.write_header(Header(flags, len(body_data)))
        self._stream.stream.write(body_data)
