from django.db import models
from . import Teacher, School


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=False, null=False)
    location = models.TextField(blank=False, null=False)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}: {self.location}"
