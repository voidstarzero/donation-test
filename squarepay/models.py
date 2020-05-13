from django.db import models

from cvonline.models import Attendee

from datetime import datetime
import uuid

class CardPayment(models.Model):
    amount          = models.IntegerField( null=False, blank=False)
    idempotency_key = models.CharField(max_length=64, default=uuid.uuid1) # Square API idempotency key
    attendee_payer  = models.ForeignKey(Attendee, related_name='payments',
                                                  on_delete=models.SET_NULL, null=True)
    date_paid       = models.DateTimeField(auto_now_add=True)
