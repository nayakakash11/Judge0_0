from django.db import models
from problems.models import Problem

# Create your models here.
class CodeSubmission(models.Model):
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    verdict = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Submission {self.id}"