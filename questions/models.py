from django.db import models
from accounts.models import UserProfile
import uuid as uuidlib
# Create your models here.
class Questions(models.Model):
    #uuid = models.UUIDField(default=uuidlib.uuid4,editable=False)
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="questions")
    content = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=240,unique=True)

    def __str__(self):
        return self.content

class Answers(models.Model):
    uuid = models.UUIDField(db_index=True,default=uuidlib.uuid4,editable=False)
    body = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Questions,on_delete=models.CASCADE,related_name="answers")
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    voters = models.ManyToManyField(UserProfile,related_name="votes")

    def __str__(self):
        return self.author.name
