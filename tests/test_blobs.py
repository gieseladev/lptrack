import dataclasses
import json
import pathlib
from typing import Iterator, List, Optional

import lptrack


@dataclasses.dataclass()
class BlobList:
    name: str
    blobs: List[str]


def load_blobs() -> Iterator[BlobList]:
    files = pathlib.Path("tests/data/blob").glob("*.json")
    for file in files:
        with file.open() as fp:
            data = json.load(fp)

        yield BlobList(file.stem, data)


def pytest_generate_tests(metafunc):
    def gen_id(blob_list: BlobList) -> Optional[str]:
        return blob_list.name

    if "blob_list" in metafunc.fixturenames:
        metafunc.parametrize("blob_list", load_blobs(), ids=gen_id)


def run_blob_test(blob: str) -> None:
    track = lptrack.decode(blob, string_codec=lptrack.strcodec.UTF8)
    encoded = lptrack.encode(track, string_codec=lptrack.strcodec.UTF8).decode()
    try:
        assert encoded == blob
    except AssertionError:
        print(f"track: {track}")
        raise


def test_blob_list(blob_list: BlobList):
    for blob in blob_list.blobs:
        try:
            run_blob_test(blob)
        except Exception:
            print(f"list: {blob_list.name}\n"
                  f"blob: {blob!r}")
            raise
