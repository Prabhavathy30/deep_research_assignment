from rest_framework import serializers
from .models import ResearchSession, ResearchStep, UploadedDocument, CostUsage

class ResearchStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchStep
        fields = "__all__"

class CostUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostUsage
        fields = "__all__"

class UploadedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ("id", "session", "file", "uploaded_at")
        read_only_fields = ("id", "uploaded_at")

class ResearchSessionSerializer(serializers.ModelSerializer):
    steps = ResearchStepSerializer(many=True, read_only=True)
    cost = CostUsageSerializer(read_only=True)
    documents = UploadedDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchSession
        fields = "__all__"
