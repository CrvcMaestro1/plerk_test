import uuid

from transactions.serializers import CompanySerializer


class TestCompanySerializer:

    def test_valid_company_serializer(self):
        valid_serializer_data = {
            "uuid": uuid.uuid4(),
            "name": "Didi",
        }
        serializer = CompanySerializer(data=valid_serializer_data)
        assert serializer.is_valid(raise_exception=True)
        assert serializer.validated_data["name"] == valid_serializer_data["name"]

