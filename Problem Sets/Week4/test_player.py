import unittest
import os
import json
from player import Player
from media import Media, Track, Movie


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_loadFromJson_empty_file(self):
        with open("empty.json", "w") as f:
            json.dump([], f)
        self.player.loadFromJson("empty.json")
        self.assertEqual(self.player.playlist.size, 0)
        os.remove("empty.json")

    def test_loadFromJson_empty_file(self):
        self.player.loadFromJson("base_data.json")
        self.assertEqual(self.player.playlist.size, 20)

    def test_loadFromJson_single_media(self):
        media_data = [
            {
                "wrapperType": "track",
                "kind": "song",
                "trackName": "Test Track",
                "artistName": "Test Artist",
                "releaseDate": "2022-01-01",
                "trackViewUrl": "http://example.com",
                "collectionName": "Test Album",
                "primaryGenreName": "Test Genre",
                "trackTimeMillis": 300000,
            }
        ]
        with open("single_media.json", "w") as f:
            json.dump(media_data, f)
        self.player.loadFromJson("single_media.json")
        self.assertEqual(self.player.playlist.size, 1)
        os.remove("single_media.json")

    def test_loadFromJson_multiple_media(self):
        media_data = [
            {
                "wrapperType": "track",
                "kind": "song",
                "trackName": "Test Track 1",
                "artistName": "Test Artist 1",
                "releaseDate": "2022-01-01",
                "trackViewUrl": "http://example.com/1",
                "collectionName": "Test Album 1",
                "primaryGenreName": "Test Genre 1",
                "trackTimeMillis": 300000,
            },
            {
                "wrapperType": "track",
                "kind": "song",
                "trackName": "Test Track 2",
                "artistName": "Test Artist 2",
                "releaseDate": "2022-01-02",
                "trackViewUrl": "http://example.com/2",
                "collectionName": "Test Album 2",
                "primaryGenreName": "Test Genre 2",
                "trackTimeMillis": 300000,
            },
        ]
        with open("multiple_media.json", "w") as f:
            json.dump(media_data, f)
        self.player.loadFromJson("multiple_media.json")
        self.assertEqual(self.player.playlist.size, 2)
        os.remove("multiple_media.json")

    def test_next(self):
        self.player.addMedia(Media("Test Media", "Test Artist", "2022-01-01", "http://example.com"))
        self.player.addMedia(
            Media("Test Media 2", "Test Artist 2", "2022-01-02", "http://example.com/2")
        )
        self.player.addMedia(
            Track(
                "Test Track",
                "Test Artist",
                "2022-01-01",
                "http://example.com",
                "Test Album",
                "Test Genre",
                300000,
            )
        )
        self.player.addMedia(
            Track(
                "Test Track 2",
                "Test Artist 2",
                "2022-01-02",
                "http://example.com/2",
                "Test Album 2",
                "Test Genre 2",
                300000,
            )
        )
        print(self.player.playlist)
        assert self.player.next() is True

    def test_next_dummy(self):
        self.player.addMedia(
            Movie(
                "Test Movie 1",
                "Test Artist 1",
                "2022-01-01",
                "http://example.com/1",
                "PG-13",
                120000,
            )
        )
        assert self.player.next() == False


if __name__ == "__main__":
    unittest.main()
