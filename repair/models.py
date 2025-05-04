from django.db import models

# Create your models here.
from django.db import models


class Owner(models.Model):
    txtOwnerSurname = models.CharField(max_length=30)
    txtOwnerName = models.CharField(max_length=25)
    txtOwnerSecondName = models.CharField(max_length=30)
    txtAddress = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.txtOwnerSurname}, {self.txtOwnerName}, {self.txtOwnerSecondName}"


class Flat(models.Model):
    txtFlatAddress = models.CharField(max_length=100)
    intOwnerId = models.ForeignKey(Owner, on_delete=models.PROTECT, related_name='flats')
    fltArea = models.DecimalField(max_digits=6, decimal_places=2)
    intCount = models.IntegerField()  # Количество проживающих
    intStorey = models.IntegerField()  # Этаж

    def __str__(self):
        return self.txtFlatAddress


class Worker(models.Model):
    txtWorkerSurname = models.CharField(max_length=30)
    txtWorkerName = models.CharField(max_length=25)
    txtWorkerSecondName = models.CharField(max_length=30)
    txtWorkerSpecialist = models.CharField(max_length=50)
    fltSum = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.txtWorkerSurname}, {self.txtWorkerName}, {self.txtWorkerSecondName}"


class OperationType(models.Model):
    txtOperationTypeName = models.CharField(max_length=100)
    fltOperationPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.txtOperationTypeName


class Operation(models.Model):
    intFlatId = models.ForeignKey(Flat, on_delete=models.PROTECT, related_name='operations')
    intOperationTypeId = models.ForeignKey(OperationType, on_delete=models.PROTECT, related_name='operations')
    datOperationDate = models.DateField()
    intWorkerId = models.ForeignKey(Worker, on_delete=models.PROTECT, related_name='operations')
    txtOperationDescription = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.intOperationTypeId.name} - {self.datOperationDate}"
