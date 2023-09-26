from enum import Enum

import requests


class BgpViewEndpoints(Enum):
    VIEW_ASN_DETAILS = "asn-details"


class BgpView:
    # source -> https://bgpview.docs.apiary.io/#reference/0/asn/view-asn-details

    _endpoint = 'https://api.bgpview.io'

    def view_asn_details(self, asn):
        """
            {
                status: "ok",
                status_message: "Query was successful",
                data: {
                    asn: 61138,
                    name: "ZAPPIE-HOST-AS",
                    description_short: "Zappie Host LLC",
                    description_full: [
                        "Zappie Host LLC"
                    ],
                    country_code: "GB",
                    website: "https://zappiehost.com/",
                    email_contacts: [
                        "abuse@zappiehost.com",
                        "admin@zappiehost.com",
                        "noc@zappiehost.com"
                    ],
                    abuse_contacts: [
                        "abuse@zappiehost.com"
                    ]
                }
            }
        """
        return self._generate_request(f'/asn/{asn}')

    def _generate_request(self, path, **kwargs):
        return requests.get(f'{self._endpoint}/{path}', params=kwargs)
