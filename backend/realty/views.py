from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Manager, AgreementNumber, Client, ApartmentStatus, ObjectName, Apartment, PurchaseStatus
from .serializers import (ManagerSerializer, AgreementNumberSerializer, ClientSerializer, ApartmentStatusSerializer,
                          ObjectNameSerializer, ApartmentSerializer, PurchaseStatusSerializer)


class ManagerViewSet(viewsets.ModelViewSet):
    """
    API для управления данными о Менеджерах.

    Операции:
    - Список менеджеров: GET /api/managers/
    - Детали менеджера: GET /api/managers/{id}/
    - Создание менеджера: POST /api/managers/
    - Обновление менеджера: PUT /api/managers/{id}/
    - Удаление менеджера: DELETE /api/managers/{id}/
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class AgreementNumberViewSet(viewsets.ModelViewSet):
    """
    API для управления данными о Номерах Договоров.

    Операции:
    - Список номеров договоров: GET /api/agreement_numbers/
    - Детали номера договора: GET /api/agreement_numbers/{id}/
    - Создание номера договора: POST /api/agreement_numbers/
    - Обновление номера договора: PUT /api/agreement_numbers/{id}/
    - Удаление номера договора: DELETE /api/agreement_numbers/{id}/
    """
    # permission_classes = [IsAuthenticated]
    queryset = AgreementNumber.objects.all()
    serializer_class = AgreementNumberSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    API для управления данными о Клиентах.

    Операции:
    - Список клиентов: GET /api/clients/
    - Детали клиента: GET /api/clients/{id}/
    - Создание клиента: POST /api/clients/
    - Обновление клиента: PUT /api/clients/{id}/
    - Удаление клиента: DELETE /api/clients/{id}/
    """
    # permission_classes = [IsAuthenticated]
    queryset = Client.objects.select_related('agreement_number')
    serializer_class = ClientSerializer


class ApartmentStatusViewSet(viewsets.ModelViewSet):
    """
    API для управления данными о Статусах Квартир.

    Операции:
    - Список статусов квартир: GET /api/apartment_statuses/
    - Детали статуса квартиры: GET /api/apartment_statuses/{id}/
    - Создание статуса квартиры: POST /api/apartment_statuses/
    - Обновление статуса квартиры: PUT /api/apartment_statuses/{id}/
    - Удаление статуса квартиры: DELETE /api/apartment_statuses/{id}/
    """
    # permission_classes = [IsAuthenticated]
    queryset = ApartmentStatus.objects.all()
    serializer_class = ApartmentStatusSerializer


class ObjectNameViewSet(viewsets.ModelViewSet):
    """
    API для управления данными об Названиях Объектов.

    Операции:
    - Список названий объектов: GET /api/object_names/
    - Детали названия объекта: GET /api/object_names/{id}/
    - Создание названия объекта: POST /api/object_names/
    - Обновление названия объекта: PUT /api/object_names/{id}/
    - Удаление названия объекта: DELETE /api/object_names/{id}/
    """
    # permission_classes = [IsAuthenticated]
    queryset = ObjectName.objects.all()
    serializer_class = ObjectNameSerializer


class ApartmentViewSet(viewsets.ModelViewSet):
    """
    API для управления данными о Квартирах.

    Операции:
    - Список квартир: GET /api/apartments/
    - Детали квартиры: GET /api/apartments/{id}/
    - Создание квартиры: POST /api/apartments/
    - Обновление квартиры: PUT /api/apartments/{id}/
    - Удаление квартиры: DELETE /api/apartments/{id}/
    """
    # permission_classes = [IsAuthenticated]
    queryset = Apartment.objects.select_related('object_name', 'apartment_status')
    serializer_class = ApartmentSerializer


class PurchaseStatusViewSet(viewsets.ModelViewSet):
    """
    API для управления данными о Статусах Покупок.

    Операции:
    - Список статусов покупок: GET /api/purchase_statuses/
    - Детали статуса покупки: GET /api/purchase_statuses/{id}/
    - Создание статуса покупки: POST /api/purchase_statuses/
    - Обновление статуса покупки: PUT /api/purchase_statuses/{id}/
    - Удаление статуса покупки: DELETE /api/purchase_statuses/{id}/
    """
    # permission_classes = [IsAuthenticated]
    queryset = PurchaseStatus.objects.select_related('manager', 'apartment', 'client')
    serializer_class = PurchaseStatusSerializer
