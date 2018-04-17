from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return "{} група".format(self.name)
