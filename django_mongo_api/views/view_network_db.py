import datetime
import json
from enum import Enum

import stix2
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_mongo_api.models.models_stix import OrganizationStix, StixAutonomousSystem, StixObject, \
    OrganizationStixRelationship
from django_mongo_api.tools.network_db import NetworkDB, NetworkDBEndpoints


class NetworkDBView(APIView):
    def __init__(self):
        self.network_db = NetworkDB()
        super().__init__()

    def get(self, request, *args, **kwargs):

        # grab our organization
        organization = OrganizationStix.objects.first()

        # which network db endpoint to use
        endpoint = kwargs.get('endpoint', None)

        # whether to take the results from the API request and
        # store it as stix
        convert_to_stix = request.query_params.get('convert-to-stix', False)

        result = None
        try:
            if endpoint == NetworkDBEndpoints.ORG_SEARCH.value:
                result = self.org_search(request=request, convert_to_stix=convert_to_stix, organization=organization)
            elif endpoint == NetworkDBEndpoints.IP_GEOLOCATION.value:
                result = self.ip_geolocation(request=request, convert_to_stix=convert_to_stix)
            elif endpoint == NetworkDBEndpoints.ORG_NETWORKS.value:
                result = self.org_networks(request=request, convert_to_stix=convert_to_stix)
            else:
                return Response({"error": "Invalid value for endpoint"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result.json(), status=result.status_code)

    def ip_geolocation(self, request, convert_to_stix):
        ip_address = request.query_params.get('ip', None)
        if ip_address is None:
            # todo get stored stix ip addresses
            pass

        result = self.network_db.ip_geolocation(ip=ip_address)
        if convert_to_stix:
            # todo implement stix
            pass

        return result

    def org_search(self, request, convert_to_stix, organization):
        org_id = request.query_params.get('org-id', None)
        if not org_id:
            raise ValueError("Invalid value for org-id")

        result = self.network_db.organization_search(organization_id=org_id)
        if convert_to_stix and result.status_code == 200:
            response = result.json()
            created_asn_stix = []
            for asn in response.get('asns', []):
                asn_stix = stix2.v21.AutonomousSystem(number=asn)

                serialized = json.loads(asn_stix.serialize())
                embedded_stix_object = StixAutonomousSystem(**serialized)
                stix_object = StixObject(
                    id=serialized.get('id'),
                    type=serialized.get('type'),
                    stix=embedded_stix_object,
                    expired=False
                ).save()


                serialized_relationship = json.loads(
                    stix2.Relationship(
                        source_ref=organization.id,
                        target_ref=stix_object.id,
                        relationship_type="uses"
                    ).serialize()
                )


                OrganizationStixRelationship(
                    id=serialized_relationship.get('id'),
                    created=datetime.datetime.utcnow(),
                    source_ref=organization,
                    target_ref=stix_object,
                    relationship_type='uses'
                ).save()





        return result

    def org_networks(self, request, convert_to_stix):
        org_id = request.query_params.get('org-id', None)
        if not org_id:
            raise ValueError("Invalid value for org-id")

        result = self.network_db.organization_networks(organization_id=org_id)
        if convert_to_stix:
            # todo implement stix
            pass

        return result