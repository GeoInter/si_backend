from django.db import models
from django.utils.translation import gettext_lazy as _

class Strategy(models.Model):
    player_cards = models.CharField(max_length=5)
    dealer_cards = models.CharField(max_length=2)
    action = models.PositiveSmallIntegerField()
    rulesetId = models.PositiveSmallIntegerField()

