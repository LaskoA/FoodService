from rest_framework import serializers
from app.models import Printer, Check


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ("id", "name", "api_key", "check_type", "point_id")


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ("id", "printer_id", "type", "order", "status", "pdf_file")
