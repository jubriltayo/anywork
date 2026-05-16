from rest_framework import serializers
from .models import Location, Category, Job



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    # READ (frontend display)
    location = LocationSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    # WRITE (frontend sends IDs)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source="location",
        write_only=True
    )

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Job
        fields = [
            "job_id",
            "employer",
            "title",
            "description",

            "location",
            "location_id",

            "category",
            "category_id",

            "salary_range",
            "job_type",
            "posted_at",
            "expires_at",
            "is_active",
        ]
        read_only_fields = ["job_id", "posted_at", "employer"]
