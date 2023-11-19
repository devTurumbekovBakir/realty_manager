from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import (ManagerViewSet, AgreementNumberViewSet, ClientViewSet, ApartmentStatusViewSet, ObjectNameViewSet,
                    ApartmentViewSet, PurchaseStatusViewSet)

router = routers.DefaultRouter()
router.register('managers', ManagerViewSet)
router.register('agreement_numbers', AgreementNumberViewSet)
router.register('clients', ClientViewSet)
router.register('apartment_statuses', ApartmentStatusViewSet)
router.register('object_names', ObjectNameViewSet)
router.register('apartments', ApartmentViewSet)
router.register('purchase_statuses', PurchaseStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token),
]
