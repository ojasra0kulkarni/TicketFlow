from django.db import models


class Ticket(models.Model):

    PRIORITY_CHOICES = [
        ('P1', 'Critical'),
        ('P2', 'High'),
        ('P3', 'Medium'),
        ('P4', 'Low'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    ]

    ticket_id = models.CharField(max_length=50, unique=True)
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    subject = models.CharField(max_length=255)
    description = models.TextField()

    address = models.CharField(max_length=255)   # city name

    order_id = models.CharField(max_length=50)

    raised_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.subject