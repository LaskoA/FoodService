from django.db import models


class Printer(models.Model):
    class CheckTypeChoices(models.TextChoices):
        KITCHEN = "Kitchen"
        CLIENT = "Client"

    name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=255, unique=True)
    check_type = models.CharField(max_length=20, choices=CheckTypeChoices.choices)
    point_id = models.IntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Check(models.Model):
    class TypeChoices(models.TextChoices):
        KITCHEN = "Kitchen"
        CLIENT = "Client"

    class StatusChoices(models.TextChoices):
        NEW = "New"
        RENDERED = "Rendered"
        PRINTED = "Printed"

    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TypeChoices.choices)
    order = models.JSONField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default="New")
    pdf_file = models.FileField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Check ID:{self.id}"
