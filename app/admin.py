from django.contrib import admin

from app.models import Printer, Check

admin.site.register(Printer)


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_filter = ("printer_id", "type", "status")
