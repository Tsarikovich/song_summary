from typing import Any, Optional
from django.db import models
from .utils import fetch_lyrics, summarize_lyrics, extract_countries


class Song(models.Model):
    """
    Represents a song with fields for the artist name, song title, lyrics,
    a summary of the lyrics, and a list of countries mentioned in the lyrics.
    """

    artist_name: str = models.CharField(max_length=255)
    song_title: str = models.CharField(max_length=255)
    lyrics: Optional[str] = models.TextField(blank=True, null=True)
    summary: Optional[str] = models.TextField(blank=True, null=True)
    countries: Optional[str] = models.TextField(blank=True, null=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Overrides the save method to fetch lyrics, generate a summary, and extract countries
        if lyrics are not already provided.

        Args:
            *args: Positional arguments passed to the parent save method.
            **kwargs: Keyword arguments passed to the parent save method.
        """
        if not self.lyrics:
            try:
                self.lyrics = fetch_lyrics(self.artist_name, self.song_title)

                if self.lyrics:
                    self.summary = summarize_lyrics(self.lyrics)
                    self.countries = extract_countries(self.lyrics)
                else:
                    self.summary = "Lyrics not found"
                    self.countries = ""
            except Exception as e:
                print(f"Error while processing song data: {e}")
                self.summary = "Error processing song"
                self.countries = ""

        # Call the parent save method
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Returns a string representation of the song.

        Returns:
            str: A formatted string with the artist's name and song title.
        """
        return f"{self.artist_name} - {self.song_title}"