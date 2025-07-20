from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=100)
    statement = models.TextField()

    def __str__(self):
        return self.title
    

