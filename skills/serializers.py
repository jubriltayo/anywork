from rest_framework import serializers

from .models import Skill



class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ['skill_id', 'user']
