from rest_framework.response import Response
from rest_framework import views

from transactions import models


class SummaryAPIView(views.APIView):
    model_class = models.Summary()

    def get(self, request):
        summary = self.model_class.get_summary()
        return Response(summary)
