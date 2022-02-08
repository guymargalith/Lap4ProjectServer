from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     user_name = models.CharField(max_length=120,unique = True)
#     email = models.EmailField(unique = True, null = False)
#     password = models.CharField(max_length=100, null = False)
#     account_type = models.IntegerField()

#     def __str__(self):
#         return f'{self.user_name}, {self.email}, {self.password}, {self.account_type}'


class Competition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=500)
    units = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    type_of_competition = models.IntegerField()
    end_date = models.DateField(null=False)
    host_id = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.name}, {self.description}, {self.units}, {self.frequency}, {self.type_of_competition}, {self.end_date}, {self.host_id}, {self.completed}'

class Score(models.Model):
    id = models.AutoField(primary_key=True)
    competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="scores")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores_user")
    score = models.IntegerField()
    last_updated = models.DateField()

    class Meta:
        unique_together = ['competition_id', 'user_id']

    def __unicode__(self):
        return '%s' %(self.score)
