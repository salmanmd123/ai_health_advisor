from django.db import models


class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=20, default='activated')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_registration'

    def __str__(self):
        return f"{self.name} ({self.loginid})"


class SymptomCheckHistory(models.Model):
    user = models.ForeignKey(UserRegistrationModel, on_delete=models.CASCADE, null=True, blank=True)
    symptoms_input = models.TextField()
    detected_symptoms = models.TextField()
    possible_conditions = models.TextField()
    advice = models.TextField()
    severity = models.CharField(max_length=20, default='mild')
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'symptom_check_history'
        ordering = ['-checked_at']

    def __str__(self):
        return f"Check by {self.user} on {self.checked_at.strftime('%Y-%m-%d')}"


class AdminRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'admin_registration'

    def __str__(self):
        return self.name
