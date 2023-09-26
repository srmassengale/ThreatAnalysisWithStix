from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_mongo_api.models.models_stix import OrganizationStix
from django_mongo_api.tools.bgp_view import BgpView, BgpViewEndpoints


class BgpViewView(APIView):
    def __init__(self):
        self.bgp_view = BgpView()
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
            if endpoint == BgpViewEndpoints.VIEW_ASN_DETAILS.value:
                result = self.view_asn_details(request=request, convert_to_stix=convert_to_stix)
            else:
                return Response({"error": "Invalid value for endpoint"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result.json(), status=result.status_code)

    def view_asn_details(self, request, convert_to_stix):
        asn = request.query_params.get('asn', None)
        if not asn:
            # todo grab existing asns
            pass

        result = self.bgp_view.view_asn_details(asn=asn)
        if convert_to_stix:
            # todo implement stix
            pass

        return result