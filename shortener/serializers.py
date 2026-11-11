from urllib.parse import urlparse

from rest_framework import serializers

ALLOWED_SCHEMES = {"http", "https"}


class ShortenSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=2048)

    def validate_url(self, value: str) -> str:
        if urlparse(value).scheme not in ALLOWED_SCHEMES:
            raise serializers.ValidationError("Only http and https URLs are allowed.")
        return value
