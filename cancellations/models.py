from django.db import models
from django.db.models import Q


class CancellationManager(models.Manager):

    def get_queryset(self):
        
        return super(CancellationManager, self).get_queryset().filter(Q(client__cancelled="Cancelled") | Q(sale__cancelled="Cancelled"))



class Cancellation(models.Model):
    YES = 'YES'
    NO = 'NO'
    DEBATIBLE = 'DEBATIBLE'

    FAIL_CHOICES = (
        (YES, ('YES')),
        (NO, ('NO')),
        (DEBATIBLE, ('DEBATIBLE')),
        )
    
    objects = CancellationManager()
    id_can = models.AutoField(primary_key=True)
    comment_can = models.CharField(max_length=500, blank=True, null=True, verbose_name="COMMENT")
    date_can = models.DateField(null=True, blank=True, verbose_name="DATE")
    fail_can = models.CharField(max_length=50, choices=FAIL_CHOICES, blank=True, null=True, verbose_name="DO WE FAIL?")
    
    def __str__ (self):
        try:
            return str(self.client.customer)
        except:
            return '{} - {}'.format(self.sale.service, self.sale.account)


