from lyrics.utils import fetch_lyrics, summarize_lyrics


def test_fetch_lyrics_success(requests_mock):
    artist = "Adele"
    title = "Hello"
    mocked_url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"

    requests_mock.get(
        mocked_url,
        json={
            "message": {
                "header": {"status_code": 200},
                "body": {"lyrics": {"lyrics_body": "Hello, it's me, I was wondering..."}},
            }
        },
    )

    lyrics = fetch_lyrics(artist, title)
    assert lyrics == "Hello, it's me, I was wondering..."


def test_fetch_lyrics_not_found(requests_mock):
    artist = "Unknown"
    title = "NoSong"
    mocked_url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"

    requests_mock.get(
        mocked_url,
        json={
            "message": {
                "header": {"status_code": 404},
                "body": {},
            }
        },
    )

    lyrics = fetch_lyrics(artist, title)
    assert lyrics is None

def test_summarize_lyrics_no_lyrics():
    summary = summarize_lyrics("")
    assert summary == "No lyrics provided."

