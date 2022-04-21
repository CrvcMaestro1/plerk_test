import csv
import os
from decimal import Decimal

import django
from django.utils.dateparse import parse_datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plerk_test.settings")
django.setup()

from transactions import models


class ImportFixture:

    def __init__(self, length_complete_transaction):
        self.path = "fixed_test_database.csv"
        self.length_complete_transaction = length_complete_transaction
        self.index = {
            "company": 0, "price": 1, "date": 2, "status_transaction": 3, "status_approved": 4
        }

    @staticmethod
    def get_or_create_company(name):
        name = name.capitalize()
        if not models.Company.objects.filter(name__exact=name).exists():
            company = models.Company(name=name)
            company.save()
        else:
            company = models.Company.objects.filter(name__exact=name).last()
        if not company:
            raise Exception('Company doesnt found, {}'.format(name))
        return company

    @staticmethod
    def is_valid_status_transaction(status):
        return status in models.TransactionStatus

    @staticmethod
    def get_status_cashed(transaction):
        return transaction.status_transaction == models.TransactionStatus.closed and transaction.status_approved is True

    def do_not_import_if_already_import(self):
        with open(self.path, newline='', encoding='utf-8') as file:
            csvreader = csv.reader(file)
            next(csvreader)
            number_rows = sum(1 for row in csvreader)
            return models.Transaction.objects.count() == number_rows

    def save_transaction(self):
        rows = 0
        with open(self.path, newline='', encoding='utf-8') as file:
            csvreader = csv.reader(file)
            next(csvreader)
            if self.do_not_import_if_already_import():
                raise Exception('All fixtures were already imported')
            for row in csvreader:
                row_length = len(row)
                if row_length == self.length_complete_transaction:
                    company = self.get_or_create_company(
                        row[self.index["company"]]
                    )
                    if not self.is_valid_status_transaction(row[self.index["status_transaction"]]):
                        raise Exception('Invalid status_transaction, {}'.format(row))
                    transaction = models.Transaction(
                        company=company, price=Decimal(row[self.index["price"]]),
                        date=parse_datetime(row[self.index["date"]]),
                        status_transaction=row[self.index["status_transaction"]],
                        status_approved=True if row[self.index["status_approved"]] == "true" else False
                    )
                    transaction.status_cashed = self.get_status_cashed(transaction)
                    transaction.save()
                    rows += 1
        return rows


if __name__ == '__main__':
    import_fixtures = ImportFixture(5)
    rows_imported = import_fixtures.save_transaction()
    print('{} fixtures were imported'.format(rows_imported))
