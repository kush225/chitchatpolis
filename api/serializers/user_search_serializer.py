from rest_framework import serializers

class SanitizedCharField(serializers.CharField):
    """
    Custom CharField that sanitizes the input by removing leading and trailing whitespaces,
    and reducing consecutive whitespaces between words to a single space.
    """

    def to_internal_value(self, data: str) -> str:
        """
        Convert input data to its internal representation after sanitization.
        """
        # Remove leading and trailing whitespaces
        data = data.strip()
        # Remove extra whitespaces between words
        data = ' '.join(data.split())
        return super().to_internal_value(data)


class UserSearchSerializer(serializers.Serializer):
    """
    Serializer for search functionality to sanitize the search keyword.
    """

    search_keyword = SanitizedCharField(max_length=100)
