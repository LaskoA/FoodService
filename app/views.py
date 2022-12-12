import json
import requests
import jinja2
import pdfkit
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import mixins, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.models import Printer, Check

from app.serializers import PrinterSerializer, CheckSerializer


class PrinterViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class CheckViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer


@api_view(["GET"])
def orders(self):
    """GET JSON with dummy orders, which will be used by create_check function"""

    with open('order_sample.json') as file:
        data = json.load(file)
        return Response(data=data)


@api_view(["POST"])
def create_check(self):
    """This function receives JSON with orders from another API and creates checks in our DB. If printer is not found
    or orders exists already, error will be raised. PDFs for checks are also created and stored in .media/pdf folder"""

    orders_response = requests.get("http://127.0.0.1:8000/app/orders/").json()
    all_checks = Check.objects.all()
    order_ids = []

    for check in all_checks:
        order_ids.append(check.order["id"])

    for item in orders_response["orders"]:
        if item["id"] in order_ids:
            raise ValidationError(f"Order #{item['id']} already exists")

        try:
            Printer.objects.get(pk=item["point_id"])
        except ObjectDoesNotExist:
            raise ValidationError("printer with such ID does not exist")

        printers = Printer.objects.filter(point_id=item["point_id"])

        for printer in printers:

            order_id = item["id"]
            date = item["date"]
            items = item["items"]
            total = item["total"]
            address = item["address"]
            point_id = item["point_id"]

            context = {
                "order_id": order_id,
                "date": date,
                "items": items,
                "total": total,
                "address": address,
                "point_id": point_id
            }

            template_loader = jinja2.FileSystemLoader("templates")
            template_env = jinja2.Environment(loader=template_loader)

            template = template_env.get_template("check_template.html")
            output_text = template.render(context)

            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

            pdfkit.from_string(output_text, f"media/pdf/{order_id}_{printer.check_type}.pdf", configuration=config)
            check = Check(
                printer_id=Printer.objects.get(id=printer.id),
                type=printer.check_type,
                order=item,
                status="Rendered",
                pdf_file=f"media/pdf/{order_id}_{printer.check_type}.pdf")
            check.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
def print_check(self):
    """Change status to 'printed' for all existing checks"""

    queryset = Check.objects.all()
    for q in queryset:
        q.status = "Printed"
        q.save()

    return Response(status=status.HTTP_200_OK)
