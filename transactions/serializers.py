from rest_framework import serializers

from transactions.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name",)


class CompanyByIdSerializer(serializers.Serializer):
    name = serializers.CharField()
    number_cashed_transactions = serializers.IntegerField(default=0)
    number_not_cashed_transactions = serializers.IntegerField(default=0)
    date_of_most_transactions = serializers.CharField()
    times = serializers.IntegerField(default=0)

    def update(self, instance, validated_data):
        raise NotImplemented()

    def create(self, validated_data):
        raise NotImplemented()
