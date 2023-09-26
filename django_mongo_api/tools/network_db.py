from enum import Enum

import requests


class NetworkDBEndpoints(Enum):
    IP_GEOLOCATION = "ip-geolocation"
    ORG_SEARCH = 'org-search'
    ORG_NETWORKS = 'org-networks'

class NetworkDB:

    # source -> https://networksdb.io/api/docs#orgsearch

    _endpoint = 'https://networksdb.io/api'
    _api_key = '6c6694f1-4019-492b-be62-a376bf6c3649'

    def organization_search(self, organization_id):
        """
            organization_id: param -> american association of registered ....
            {
                "organization": "Google LLC",
                "id": "google-llc",
                "address": null,
                "phone": null,
                "countries": [
                    "United States",
                    "Japan",
                    "Thailand"
                ],
                "networks": {
                    "ipv4": 238,
                    "ipv6": 41
                },
                "networks_by_country": {
                    "United States": 289,
                    "Japan": 2,
                    "Thailand": 2
                },
                "url": "https://networksdb.io/ip-addresses-of/google-llc",
                "asns": [
                    "15169"
                ]
            }


        """
        return self._generate_request('org-info', id=organization_id)

    def organization_networks(self, organization_id):
        """
        {
            "total": 238,
            "page": 1,
            "results": [
                {
                    "netname": "GOOGL-2",
                    "description": "Google LLC",
                    "extrainfo": "",
                    "countrycode": "US",
                    "country": "United States",
                    "blocksize": "4194304",
                    "cidr": "34.64.0.0/10",
                    "first_ip": "34.64.0.0",
                    "last_ip": "34.127.255.255"
                }
            ]
        }
        """
        return self._generate_request('org-networks', id=organization_id)

    def ip_geolocation(self, ip):
        """
        ip: param -> ipv4 address
        returns:

        {
            "ip": "8.8.8.8",
            "continent": "North America",
            "countrycode": "US",
            "country": "United States",
            "state": "California",
            "city": "Mountain View",
            "latitude": 37.406,
            "longitude": -122.079
        }

        """
        return self._generate_request('ip-geo', ip=ip)

    def _generate_request(self, path, **kwargs):
        headers = {
            'X-Api-Key': self._api_key
        }

        return requests.get(f'{self._endpoint}/{path}', headers=headers, params=kwargs)
