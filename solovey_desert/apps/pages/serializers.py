from rest_framework import serializers

from apps.catalog.serializers import absolute_file_url

from .models import HeroSlide


class HeroSlideSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSlide
        fields = (
            'id',
            'eyebrow',
            'title',
            'subtitle',
            'image_url',
            'primary_button_text',
            'primary_button_url',
            'secondary_button_text',
            'secondary_button_url',
            'order',
        )

    def get_image_url(self, obj):
        return absolute_file_url(self.context.get('request'), obj.image)
