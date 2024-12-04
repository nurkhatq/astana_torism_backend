from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from places.serializers import PlaceSerializer, ReviewSerializer
User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    favorite_places_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'avatar', 'bio', 'phone_number', 'date_of_birth',
            'country', 'city', 'preferred_language',
            'instagram', 'facebook', 'twitter',
            'review_count', 'favorite_places_count', 'date_joined', 'favorite_places'
        )
        read_only_fields = ('id', 'username', 'email', 'date_joined')

    def update(self, instance, validated_data):
        # Explicitly update each field
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.preferred_language = validated_data.get('preferred_language', instance.preferred_language)
        instance.instagram = validated_data.get('instagram', instance.instagram)
        instance.facebook = validated_data.get('facebook', instance.facebook)
        instance.twitter = validated_data.get('twitter', instance.twitter)

        instance.save()
        return instance
        
    def get_review_count(self, obj):
        return obj.get_review_count()
        
    def get_favorite_places_count(self, obj):
        return obj.get_favorite_places_count()
class UserDetailSerializer(UserProfileSerializer):
    favorite_places = PlaceSerializer(many=True, read_only=True)
    recent_reviews = serializers.SerializerMethodField()
    
    class Meta(UserProfileSerializer.Meta):
        fields = UserProfileSerializer.Meta.fields + (
            'favorite_places', 'recent_reviews'
        )
        
    def get_recent_reviews(self, obj):
        recent_reviews = obj.reviews.order_by('-created_at')[:5]
        return ReviewSerializer(recent_reviews, many=True).data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 
                 'last_name', 'phone_number')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user