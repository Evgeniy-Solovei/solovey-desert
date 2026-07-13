from rest_framework import serializers

from .models import Category, Product, ProductImage, ProductWeightOption


def absolute_file_url(request, file_field):
    if not file_field:
        return ''
    url = file_field.url
    return request.build_absolute_uri(url) if request else url


class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'image_url',
            'url',
            'is_featured',
            'order',
        )

    def get_image_url(self, obj):
        return absolute_file_url(self.context.get('request'), obj.image)


class ProductWeightOptionSerializer(serializers.ModelSerializer):
    weight_label = serializers.CharField(read_only=True)

    class Meta:
        model = ProductWeightOption
        fields = ('id', 'weight', 'weight_unit', 'weight_label', 'price', 'is_default', 'order')


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('id', 'image_url', 'alt', 'order')

    def get_image_url(self, obj):
        return absolute_file_url(self.context.get('request'), obj.image)


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    main_image_url = serializers.SerializerMethodField()
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    default_weight_option = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'slug',
            'category',
            'short_description',
            'main_image_url',
            'price_from',
            'is_featured',
            'url',
            'default_weight_option',
        )

    def get_main_image_url(self, obj):
        return absolute_file_url(self.context.get('request'), obj.main_image)

    def get_default_weight_option(self, obj):
        option = next((item for item in obj.weight_options.all() if item.is_default), None)
        option = option or next(iter(obj.weight_options.all()), None)
        if not option:
            return None
        return ProductWeightOptionSerializer(option).data


class ProductDetailSerializer(ProductListSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    weight_options = ProductWeightOptionSerializer(many=True, read_only=True)

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + (
            'description',
            'taste_description',
            'composition',
            'note',
            'images',
            'weight_options',
        )
