from rest_framework import serializers

from . models import Profile


class ProfileMarksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['get_json_marks', ]
