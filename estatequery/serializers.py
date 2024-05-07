from rest_framework import serializers
from .models import RealEstate

class RealEstateSerializer(serializers.ModelSerializer):
    realtor_email = serializers.EmailField(source="realtor.email", read_only=True)
    class Meta:
        model = RealEstate
        fields = ["id", "realtor", "realtor_email", "title", "slug", "created_at", "modified_at", "price", "currency", "street_address", "city", "state", "country", "zipcode", "area_value", "area_unit", "rent_or_sale_status", "type", "is_available","available_date", "no_of_bedrooms", "no_of_bathrooms", "is_parking", "facilities", "nearby_places", "overview", "main_photo", "photo_one", "photo_two", "photo_three", "is_published"]
        read_only = ["id", "created_at", "modified_at"]