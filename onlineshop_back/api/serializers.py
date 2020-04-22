from rest_framework import serializers
from api.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    description = serializers.CharField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image', 'color', 'size', 'category')


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        company = Category.objects.create(name=validated_data.get('name'))
        return company

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
