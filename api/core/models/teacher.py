from django.db import models
from . import School


class Teacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=False, null=False)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
