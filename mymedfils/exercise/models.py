from django.db import models

# Create your models here.
class Member(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	mobile = models.IntegerField()
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.name
