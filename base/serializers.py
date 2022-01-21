from rest_framework import serializers
from .models import Section, Audio

class SectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

class AudioLatinSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name_latin = serializers.CharField(read_only=True)
    audio_true = serializers.BooleanField(read_only=True)
    file = serializers.FileField(read_only=True)
    youtube_id = serializers.CharField(read_only=True)
    section = serializers.CharField(read_only=True)

class AudioCyrillicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name_cyrillic = serializers.CharField(read_only=True)
    audio_true = serializers.BooleanField(read_only=True)
    file = serializers.FileField(read_only=True)
    youtube_id = serializers.CharField(read_only=True)
    section = serializers.CharField(read_only=True)
