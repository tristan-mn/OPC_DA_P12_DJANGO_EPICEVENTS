from django.db import models

from authentication.models import CustomUser


class Client(models.Model):

    class ClientStatus(models.TextChoices):
        existing_client = "Existing client"
        potential_client = "Potential client"

    sales_contact = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=False, related_name='seller')
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=False)
    email = models.EmailField(max_length=100, null=False)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=20, unique=True, null=True, blank=True)
    company_name = models.CharField(max_length=250, null=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    client_status = models.CharField(max_length=64, choices=ClientStatus.choices, verbose_name='client status')

    def __str__(self):
        return f"Client: {self.last_name} | Company: {self.company_name} | Status : {self.client_status}"


class Contract(models.Model):
    sales_contact = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=False,related_name='contract_sales_staff')
    client = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=False,related_name='contract_client')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    amount = models.FloatField()
    status = models.BooleanField(default=False, verbose_name='sign')
    payment_due = models.DateField(null=True)

    def __str__(self):
        return f"Client: {self.client} | Sign: {self.status} | seller: {self.sales_contact}"


class ContractStatus(models.Model):
    signed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Contract status"

    def __str__(self):
        return f"Contract ID: {self.id} | Signed: {self.signed}"


class Event(models.Model):

    client = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=False, related_name='event_client')
    support_contact = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=False,related_name='event_support_contact')
    event_contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE, null=True, blank=True)
    event_status = models.ForeignKey(to=ContractStatus, on_delete=models.CASCADE, null=False, related_name='event_client')
    event_date = models.DateTimeField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    attendees = models.IntegerField()
    notes = models.CharField(max_length=2048)

    def __str__(self):
        return f"Client: {self.client} | Status: {self.status} | Support contact: {self.support_contact}"