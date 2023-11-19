from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class Manager(AbstractUser):
    """
        Пользовательская модель представляющая менеджера в системе.

        Атрибуты:
            full_name (str): Полное имя менеджера.
            phone_number (str): Уникальный номер телефона менеджера (должен начинаться с +996 и содержать только цифры).
            created_at (date): Дата создания менеджера (автоматически генерируется при создании).
            date_updated (datetime): Дата и время последнего обновления (автоматически обновляется при каждом изменении).
            amount_of_deals (int): Общее количество сделок, связанных с менеджером (по умолчанию 0).

        Методы:
            __str__(): Возвращает отформатированную строку представления менеджера.

            calculate_total_deals(): Вычисляет и возвращает общее количество сделок, связанных с менеджером.
        """

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13, unique=True)
    created_at = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    amount_of_deals = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

    def __str__(self):
        return f'{self.full_name} - {self.phone_number}'

    def calculate_total_deals(self):
        return self.purchase_statuses.count()


class AgreementNumber(models.Model):
    """
        Модель Номера Договора.

        Поля:
        - name (str): Название договора.
        - number (int): Уникальный номер договора.

        Методы:
        - __str__(): Возвращает строковое представление номера договора.
    """

    name = models.TextField()
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name = '№ Договора'
        verbose_name_plural = '№ Договоров'


class Client(models.Model):
    """
        Модель Клиента.

        Поля:
        - full_name (str): Полное имя клиента.
        - passport_id (str): Паспортные данные клиента.
        - phone_number (str): Номер телефона клиента.
        - agreement_number (AgreementNumber): Номер договора, связанный с клиентом.

        Методы:
        - __str__(): Возвращает строковое представление клиента.
    """

    full_name = models.CharField(max_length=50)
    passport_id = models.CharField(max_length=9, unique=True, db_index=True)
    phone_number = models.CharField(max_length=13, unique=True)
    agreement_number = models.ForeignKey(AgreementNumber, on_delete=models.PROTECT)
    ...

    def __str__(self):
        return f'{self.full_name} - {self.phone_number}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class ApartmentStatus(models.Model):
    """
        Модель Статуса Квартиры.

        Поля:
        - name (str): Название статуса квартиры.

        Методы:
        - __str__(): Возвращает строковое представление статуса квартиры.
    """

    name = models.CharField(max_length=30)
    ...

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Статус Квартиры'
        verbose_name_plural = 'Статусы Квартир'


class ObjectName(models.Model):
    """
        Модель Названия Объекта.

        Поля:
        - name (str): Название объекта.
        - address (str): Адрес объекта.

        Методы:
        - __str__(): Возвращает строковое представление объекта.
    """

    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Название Объекта'
        verbose_name_plural = 'Названия Объектов'


class Apartment(models.Model):
    """
        Модель Квартиры.

        Поля:
        - number (int): Уникальный номер квартиры.
        - object_name (ObjectName): Объект, к которому принадлежит квартира.
        - floor (int): Этаж квартиры.
        - area (float): Площадь квартиры.
        - created_at (date): Дата создания записи о квартире.
        - date_updated (datetime): Дата и время последнего обновления записи.
        - apartment_status (ApartmentStatus): Статус квартиры.
        - price (Decimal): Стоимость квартиры.

        Методы:
        - __str__(): Возвращает строковое представление квартиры.
    """

    number = models.CharField(max_length=5)
    object_name = models.ForeignKey(ObjectName, on_delete=models.PROTECT)
    floor = models.CharField(max_length=5)
    area = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    apartment_status = models.ForeignKey(ApartmentStatus, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.number} - {self.object_name}'

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        indexes = [
            models.Index(fields=['price', 'object_name'])  # индексация сочетание полей
        ]


class PurchaseStatus(models.Model):
    """
        Модель Статуса Покупки.

        Поля:
        - manager (Manager): Менеджер, связанный с статусом покупки.
        - apartment (Apartment): Квартира, связанная с статусом покупки.
        - client (Client): Клиент, связанный с статусом покупки.
        - date (datetime): Дата и время статуса покупки.

        Методы:
        - __str__(): Возвращает строковое представление статуса покупки.
        - save(*args, **kwargs): Переопределяет метод сохранения для обновления общего количества сделок менеджера
          после сохранения.
    """

    manager = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name='purchase_statuses', db_index=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_index=True)
    date = models.DateTimeField()
    ...

    def __str__(self):
        return f'{self.apartment} - {self.client}'

    class Meta:
        verbose_name = 'Статус Покупки'
        verbose_name_plural = 'Статус Покупок'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Manager.objects.filter(pk=self.manager.pk).update(amount_of_deals=F('amount_of_deals') + 1)
