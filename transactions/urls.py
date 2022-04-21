from django.urls import path

from transactions.views import companies, summary

urlpatterns = [
    path("company/", companies.CompaniesAPIView.as_view(), name="view-company"),
    path("company/<uuid:pk>", companies.CompanyByIdAPIView.as_view(), name="view-company-by-id"),
    path("summary/", summary.SummaryAPIView.as_view(), name="view-summary"),
]
