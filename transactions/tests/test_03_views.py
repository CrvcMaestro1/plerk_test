import pytest
from django_mock_queries.query import MockSet, MockModel

from transactions import models
from transactions.views import companies

"""
START FIXTURES
"""


@pytest.fixture
def companies_queryset():
    qs = MockSet(
        MockModel(id="970d345f-009e-486c-8be3-f08e24f82cc5", name="Didi food"),
        MockModel(id="0d8f15f9-bb89-4636-a7ba-a7501b0afb67", name="Rappi prime"),
    )
    return qs


@pytest.fixture
def amazon_company():
    return MockModel(id="49cc0d89-ca50-44fc-81cd-313dd931b584", name="Amazon", number_cashed_transactions=114,
                     number_not_cashed_transactions=36, date_of_most_transactions="2021-06-28", times=8)


@pytest.fixture
def get_summary():
    return {
        "company_highest_sales": "Rappi", "number_highest_sales": 564,
        "company_least_sales": "Supercell videogame", "number_least_sales": 1,
        "number_cashed_transactions": 1842, "number_not_cashed_transactions": 849,
        "company_most_rejections": "Uber eats", "number_most_rejections_sales": 205
    }


"""
END FIXTURES
"""


class TestCompaniesListAPIView:

    def test_get_list(self, client, mocker, companies_queryset):
        mocker.patch.object(
            companies.CompaniesAPIView,
            "get_queryset",
            return_value=companies_queryset,
        )
        payload = [{
            "id": "970d345f-009e-486c-8be3-f08e24f82cc5",
            "name": "Didi food"
        }, {
            "id": "0d8f15f9-bb89-4636-a7ba-a7501b0afb67",
            "name": "Rappi prime"
        }]
        response = client.get("/api/company/")
        assert response.status_code == 200
        assert response.json() == payload


class TestCompanyByIdAPIView:

    def test_get_by_id(self, client, mocker, amazon_company):
        mocker.patch.object(
            companies.CompanyByIdAPIView,
            "get_object",
            return_value=amazon_company,
        )
        payload = {
            "name": "Amazon",
            "number_cashed_transactions": 114, "number_not_cashed_transactions": 36,
            "date_of_most_transactions": "2021-06-28", "times": 8
        }
        response = client.get("/api/company/{}".format("49cc0d89-ca50-44fc-81cd-313dd931b584"))
        assert response.status_code == 200
        assert response.json() == payload


class TestSummaryAPIView:

    def test_get_summary(self, client, mocker, get_summary):
        mocker.patch.object(
            models.Summary,
            "get_summary",
            return_value=get_summary,
        )
        payload = [
            "company_highest_sales", "number_highest_sales", "company_least_sales", "number_least_sales",
            "number_cashed_transactions", "number_not_cashed_transactions", "company_most_rejections",
            "number_most_rejections_sales"
        ]
        response = client.get("/api/summary/")
        assert response.status_code == 200
        assert list(response.json().keys()) == payload
