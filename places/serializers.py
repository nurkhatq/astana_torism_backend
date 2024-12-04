from rest_framework import serializers

from users.models import User
from .models import Category, Place, PlaceImage, Review
from django.db.models import Avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon']

class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['id', 'image', 'is_primary']

class UserReviewSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'avatar_url']

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
        return None

class ReviewSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer(read_only=True)
    place_id = serializers.IntegerField(source='place.id')
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'user', 'created_at', 'place_id']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        place_id = validated_data.pop('place_id')
        place = Place.objects.get(id=place_id)
        review = Review.objects.create(
            place=place,
            **validated_data
        )
        return review

class PlaceSerializer(serializers.ModelSerializer):
    images = PlaceImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)
    google_rating = serializers.FloatField(read_only=True)
    site_rating = serializers.SerializerMethodField()
    def get_site_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg']

    def get_average_rating(self, obj):
        return obj.average_rating()
    class Meta:
        model = Place
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'address', 'latitude', 'longitude', 'phone', 'website',
            'images', 'google_rating', 'site_rating', 'average_rating', 'reviews_count', 'created_at'
        ]

class PlaceDetailSerializer(PlaceSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta(PlaceSerializer.Meta):
        fields = PlaceSerializer.Meta.fields + ['reviews']