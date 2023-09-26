from django.urls import path

from django_mongo_api.tools.bgp_view import BgpView
from django_mongo_api.views.view_bgp_view import BgpViewView
from django_mongo_api.views.view_network_db import NetworkDBView
from django_mongo_api.views.view_organization import OrganizationView

urlpatterns = [
    path('organization', OrganizationView.as_view(), name='org-view'),

    path('tools/networkdb/<str:endpoint>', NetworkDBView.as_view(), name='network-dbs-view'),
    path('tools/bgpview/<str:endpoint>', BgpViewView.as_view(), name='bpg-view')

]