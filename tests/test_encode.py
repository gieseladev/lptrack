import lptrack


def test_encode():
    info = lptrack.Track(
        title="Wisin & Yandel, Romeo Santos - Aullando (Official Video)",
        author="Wisin & Yandel",
        duration=255,
        identifier="-n9krkSb-ug",
        is_stream=False,
        uri="https://www.youtube.com/watch?v=-n9krkSb-ug",
    )

    track = lptrack.encode(info)

    assert track == b"QAAAjwIAOFdpc2luICYgWWFuZGVsLCBSb21lbyBTYW50b3MgLSBBdWxsYW5kbyAoT2ZmaWNpYWwgVmlkZW8pAA5XaXNpbiAmIFlhbmRlbAAAAAAAA+QYAAstbjlrcmtTYi11ZwABACtodHRwczovL3d3dy55b3V0dWJlLmNvbS93YXRjaD92PS1uOWtya1NiLXVn"
