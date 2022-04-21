import uuid

from django.db import models
from django.db.models import Count


class TransactionStatus(models.TextChoices):
    closed = "closed", "CLOSED"
    reversed = "reversed", "REVERSED"
    pending = "pending", "PENDING"
    funding = "funding", "FUNDING"
    funding_user = "funding-user", "FUNDING-USER"


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Name", max_length=256)
    status = models.BooleanField(verbose_name="Status", default=True)

    def number_cashed_transactions(self):
        return self.transaction_set.filter(status_cashed=True).count()

    def number_not_cashed_transactions(self):
        return self.transaction_set.filter(status_cashed=False).count()

    def get_date(self):
        date = self.transaction_set.values("date__date") \
            .annotate(count=Count("id")) \
            .values("date__date", "count") \
            .order_by("count").last()
        return date

    def date_of_most_transactions(self):
        date = self.get_date()
        return "" if date is None else date["date__date"]

    def times(self):
        date = self.get_date()
        return "" if date is None else date["count"]


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    price = models.DecimalField(verbose_name="Price", max_digits=10, decimal_places=2)
    date = models.DateTimeField(verbose_name="Date")
    status_transaction = models.CharField(verbose_name="Status transaction", choices=TransactionStatus.choices,
                                          default=TransactionStatus.pending, max_length=25)
    status_approved = models.BooleanField(verbose_name="Status approved", default=False)
    status_cashed = models.BooleanField(verbose_name="Status cashed", default=False)


class Summary:
    def __init__(self):
        self.model = Transaction

    def company_highest_sales(self):
        highest_sales = self.model.objects.values("company") \
            .annotate(count=Count("id")) \
            .values("company__name", "count") \
            .order_by("count").last()
        company = {"name": "", "sales": 0}
        if highest_sales:
            company["name"] = highest_sales["company__name"]
            company["sales"] = highest_sales["count"]
        return company

    def company_least_sales(self):
        least_sales = self.model.objects.values("company") \
            .annotate(count=Count("id")) \
            .values("company__name", "count") \
            .order_by("-count").last()
        company = {"name": "", "sales": 0}
        if least_sales:
            company["name"] = least_sales["company__name"]
            company["sales"] = least_sales["count"]
        return company

    def number_cashed_transactions(self):
        return self.model.objects.filter(status_cashed=True).count()

    def number_not_cashed_transactions(self):
        return self.model.objects.filter(status_cashed=False).count()

    def company_most_rejections(self):
        rejections = self.model.objects.filter(status_cashed=False) \
            .values("company").annotate(count=Count("id")) \
            .values("company__name", "count").order_by("count").last()
        company = {"name": "", "rejections": 0}
        if rejections:
            company["name"] = rejections["company__name"]
            company["rejections"] = rejections["count"]
        return company

    def get_summary(self):
        data = {}
        highest_sales = self.company_highest_sales()
        data["company_highest_sales"] = highest_sales["name"]
        data["number_highest_sales"] = highest_sales["sales"]
        least_sales = self.company_least_sales()
        data["company_least_sales"] = least_sales["name"]
        data["number_least_sales"] = least_sales["sales"]
        data["number_cashed_transactions"] = self.number_cashed_transactions()
        data["number_not_cashed_transactions"] = self.number_not_cashed_transactions()
        most_rejections = self.company_most_rejections()
        data["company_most_rejections"] = most_rejections["name"]
        data["number_most_rejections_sales"] = most_rejections["rejections"]
        return data
