# file_sharing_app/serializers.py
from rest_framework import serializers
from .models import CustomUser, File

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'is_ops_user']
        extra_kwargs = {'password': {'write_only': True}}

class FileSerializer(serializers.ModelSerializer):
    file_type = serializers.CharField(required=True)  # Ensure file_type is required
    download_link = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'user', 'file_type', 'file_url', 'download_link']
        read_only_fields = ['user']

    def create(self, validated_data):
        # Handle file upload using DRF FileUploadParser
        file_obj = self.context['request'].data.get('file')
        validated_data['file_url'] = file_obj

        # Add back the file_type field handling
        validated_data['file_type'] = self.validated_data.get('file_type', '')

        return super().create(validated_data)

    def get_download_link(self, obj):
        # Create and return the download link here
        # You might want to generate a unique download link for each file
        return f"/download-file/{obj.id}/"
