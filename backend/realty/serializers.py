from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from realty.models import Manager, AgreementNumber, Client, ApartmentStatus, ObjectName, Apartment, PurchaseStatus


class ManagerSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели Manager.

        Поля:
            id (int): Уникальный идентификатор менеджера (только для чтения).
            username (str): Имя пользователя для аутентификации.
            password (str): Пароль для аутентификации (только для записи).
            full_name (str): Полное имя менеджера.
            phone_number (str): Номер телефона менеджера (должен начинаться с +996 и содержать только цифры).
            passport_id (str): Паспортные данные менеджера.
            email (str): Адрес электронной почты менеджера.

        Только для чтения поля:
            amount_of_deals (int): Общее количество сделок, связанных с менеджером.
            created_at (date): Дата создания менеджера.
            date_updated (datetime): Дата и время последнего обновления.

        Методы:
            validate_phone_number(value): Проверяет, что номер телефона начинается с +996 и содержит только цифры.

        Переопределенные методы:
            create(validated_data): Хэширует пароль перед созданием нового экземпляра менеджера.
            update(instance, validated_data): Хэширует пароль перед обновлением существующего экземпляра менеджера.
        """

    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Manager
        fields = ['id', 'username', 'password', 'full_name', 'phone_number', 'email']
        read_only_fields = ('amount_of_deals', 'created_at', 'date_updated')

    def validate_phone_number(self, value):
        if not value.startswith('+996') or not value.isdigit():
            raise ValidationError('Номер телефона должен начинаться с +996 и содержать только цифры')
        if len(value) > 13:
            raise ValidationError('Длина телефона не должна превышать 13 символов')
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)


class AgreementNumberSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели AgreementNumber.

        Все поля модели включены в сериализатор.
    """

    class Meta:
        model = AgreementNumber
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели Client.

        Поля:
        - agreement_number: Сериализатор номера договора
        - (все остальные поля модели Client)

        Методы валидации:
        - validate_phone_number: Проверка корректности формата и длины номера телефона
        - validate_passport_id: Проверка корректности формата и длины идентификационного номера паспорта
    """

    agreement_number = AgreementNumberSerializer()

    class Meta:
        model = Client
        fields = '__all__'

    def validate_phone_number(self, value):
        if not value.startswith('+996') or not value.isdigit():
            raise ValidationError('Номер телефона должен начинаться с +996 и содержать только цифры')
        if len(value) > 13:
            raise ValidationError('Длина телефона не должна превышать 13 символов')
        return value

    def validate_passport_id(self, value):
        if not value.startswith('ID'):
            raise ValidationError('Паспорт должен начинаться с "ID"')
        if len(value) > 9:
            raise ValidationError('Длина паспорта не должна превышать 9 символов')
        if not value[2:].isdigit():
            raise ValidationError('Паспорт должен содержать только цифры (после "ID")')
        return value


class ApartmentStatusSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели ApartmentStatus.

        Все поля модели включены в сериализатор.
    """

    class Meta:
        model = ApartmentStatus
        fields = '__all__'


class ObjectNameSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели ObjectName.

        Все поля модели включены в сериализатор.
    """

    class Meta:
        model = ObjectName
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели Apartment.

        Поля:
        - number: Номер квартиры
        - object_name: Сериализатор наименования объекта
        - floor: Этаж
        - area: Площадь квартиры
        - apartment_status: Сериализатор статуса квартиры
        - price: Цена
        - created_at: Дата создания записи (только для чтения)
        - date_updated: Дата последнего обновления записи (только для чтения)
    """

    object_name = ObjectNameSerializer()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Apartment
        fields = ['id', 'number', 'object_name', 'floor', 'area', 'apartment_status', 'price']
        read_only_fields = ('created_at', 'date_updated')


class PurchaseStatusSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели PurchaseStatus.

        Поля:
        - manager: Сериализатор менеджера
        - apartment: Сериализатор квартиры
        - client: Сериализатор клиента
        - (все остальные поля модели PurchaseStatus)
    """

    manager = ManagerSerializer()
    apartment = ApartmentSerializer()
    client = ClientSerializer()

    class Meta:
        model = PurchaseStatus
        fields = '__all__'
