from rest_framework import serializers

from .models import Reviews, Comments


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
                                            read_only=True,
                                            slug_field='username')
                                            
    class Meta:
        fields = ('__all__')
        model = Reviews


class CommentSerializer(serializers.Serializer):
    author = serializers.SlugRelatedField(
                                            read_only=True,
                                            slug_field='username')

    class Meta:
        fields = ('__all__')
        model = Comments
