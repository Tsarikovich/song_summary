from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SongSerializer
from .utils import fetch_lyrics, summarize_lyrics, extract_countries


class AddSongAPIView(APIView):
    def post(self, request: Any) -> Response:
        serializer = SongSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        song = serializer.save()
        try:
            lyrics = fetch_lyrics(song.artist_name, song.song_title)
            if not lyrics:
                return Response({"error": "Lyrics not found"}, status=status.HTTP_404_NOT_FOUND)

            song.lyrics = lyrics
            song.summary = summarize_lyrics(lyrics)
            song.countries = extract_countries(lyrics)
            song.save()
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(SongSerializer(song).data, status=status.HTTP_201_CREATED)