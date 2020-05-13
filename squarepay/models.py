from django.db import models

from cvonline.models import Attendee

from datetime import datetime
import uuid

class CardPayment(models.Model):
    amount          = models.IntegerField( null=False, blank=False)
    idempotency_key = models.CharField(max_length=64, default=uuid.uuid1) # Square API idempotency key
    attendee_payer  = models.ForeignKey(Attendee, related_name='payments',
                                                  on_delete=models.SET_NULL, null=True)
    is_paid         = models.BooleanField(blank=True, default=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_paid       = models.DateTimeField(null=True, blank=True)

    def set_paid(self):
        self.is_paid = True
        self.date_paid = datetime.now()
        self.save()
