from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import views

from transactions import serializers, models


class CompaniesAPIView(generics.ListAPIView):
    serializer_class = serializers.CompanySerializer
    queryset = models.Company.objects


class CompanyByIdAPIView(views.APIView):
    serializer_class = serializers.CompanyByIdSerializer
    model_class = models.Company.objects

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except models.Company.DoesNotExist:
            raise Http404()

    def get(self, request, pk):
        company = self.get_object(pk)
        serializer = self.serializer_class(company)
        return Response(serializer.data)
