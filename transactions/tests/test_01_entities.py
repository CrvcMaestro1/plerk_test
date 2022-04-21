from decimal import Decimal

import pytest
from django.utils import timezone

from transactions import models
from transactions.tests import mocks
from transactions.utils.check_uuid import is_valid_uuid

"""
START FIXTURES
"""


@pytest.fixture
def company():
    return models.Company(name="Didi")


@pytest.fixture
def transaction_pending(company):
    return models.Transaction(
        company=company, price=Decimal("120"), date=timezone.now(),
        status_transaction=models.TransactionStatus.pending,
        status_approved=True, status_cashed=False
    )


@pytest.fixture
def transaction_with_final_status(company):
    return models.Transaction(
        company=company, price=Decimal("50"), date=timezone.now(),
        status_transaction=models.TransactionStatus.closed,
        status_approved=True, status_cashed=True
    )


@pytest.fixture
def get_summary():
    return {
        "highest_sales": {"name": "Rappi", "sales": 564},
        "least_sales": {"name": "Supercell videogame", "sales": 1},
        "number_cashed_transactions": 1842,
        "number_not_cashed_transactions": 849,
        "most_rejections": {"name": "Uber eats", "rejections": 205},
    }


"""
END FIXTURES
"""


class TestCompany:
    def test_company_entity(self, company):
        assert company.name == "Didi"
        assert company.status

    def test_valid_uuid(self, company):
        assert is_valid_uuid(company.pk)


class TestTransaction:
    def test_transaction_entity(self, transaction_pending):
        assert transaction_pending.company is not None
        assert transaction_pending.company.name == "Didi"
        assert transaction_pending.status_transaction

    def test_status_cashed(self, transaction_with_final_status):
        assert transaction_with_final_status.status_transaction == models.TransactionStatus.closed
        assert transaction_with_final_status.status_approved
        assert transaction_with_final_status.status_cashed


class TestSummary:
    def test_summary(self, get_summary):
        summary = mocks.MockSummary()
        assert summary.get_summary() == get_summary
