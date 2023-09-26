import datetime
import json
from http import HTTPStatus

import stix2.v21
from rest_framework.response import Response
from rest_framework.views import APIView
from stix2 import properties, v21, Identity, ThreatActor, Relationship
from stix2.exceptions import InvalidValueError, MissingPropertiesError

from django_mongo_api.models.models_stix import OrganizationStix
from django_mongo_api.serializers.organization_serializer import OrganizationStixSerializer


class OrganizationView(APIView):

    def post(self, request, *args, **kwargs):
        raw_request = stix2.v21.Identity(
            name=request.data.get('name'),
            description=request.data.get('description'),
            sectors=request.data.get('sectors'),
            contact_information=request.data.get('contact_information'),
            identity_class="organization",
            roles=[]
        )

        try:
            serialized_company = json.loads(raw_request.serialize())

            if len(OrganizationStix.objects.filter(name=serialized_company.get('name'))) > 0:
                return Response(data={"error": "company exists"}, status=HTTPStatus.NOT_FOUND)

            new_org = OrganizationStix(
                id=serialized_company.get('id'),
                type=serialized_company.get('type'),
                name=serialized_company.get("name"),
                contact_information=serialized_company.get('contact_information'),
                sectors=serialized_company.get('sectors'),
                roles=serialized_company.get('role'),
                identity_class=serialized_company.get('identity_class'),
                created=datetime.datetime.utcnow()
            )

            new_org.save()
            return Response(data=OrganizationStixSerializer(new_org).data, status=HTTPStatus.OK)
        except (InvalidValueError | MissingPropertiesError) as e:
            return Response(data=e, status=HTTPStatus.BAD_REQUEST)
