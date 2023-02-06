from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Operator,Ticket


def create_operator(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='operator')
        instance.groups.add(group)
        Operator.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email = instance.email,
        )
post_save.connect(create_operator, sender=User)


