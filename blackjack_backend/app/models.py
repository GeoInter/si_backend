from django.db import models
from django.utils.translation import gettext_lazy as _

class Action1(models.Model):
    
    class ActionEnum(models.IntegerChoices):
        HOLD = 0, _('HOLD')
        DRAW = 1, _('DRAW')
        DOUBLE = 2, _('DOUBLE')
        SPLIT = 3, _('SPLIT')
    
    player_cards = models.CharField(max_length=100)
    dealer_cards = models.CharField(max_length=100)
    action = models.CharField(max_length=12, choices=ActionEnum.choices)
