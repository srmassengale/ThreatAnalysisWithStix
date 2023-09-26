from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

from django_mongo_api.models.models_stix import OrganizationStix


# Create your models here.


class OrganizationStixSerializer(DocumentSerializer):
    class Meta:
        model = OrganizationStix
        fields = '__all__'
