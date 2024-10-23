from django.db import models
from django.contrib.auth.models import User

class Clinic(models.Model):
    name = models.CharField(max_length=255)

class Attendant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    counter = models.IntegerField()  # Número do guichê do atendente

    def __str__(self):
        return f"{self.user.username} - {self.clinic.name}"

class Password(models.Model):
    number = models.IntegerField()
    counter = models.IntegerField()
    called = models.BooleanField(default=False)
    time_called = models.DateTimeField(auto_now_add=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
