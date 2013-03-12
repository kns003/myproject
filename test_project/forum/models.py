from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    thread_user = models.ForeignKey(User)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)



    def __unicode__(self):
		return self.title


class Comment(models.Model):
    commented_by = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    text = models.CharField(max_length=300)
    userUpVotes = models.IntegerField()
    userDownVotes = models.IntegerField()
    commented_at = models.DateTimeField(auto_now_add=True)
   

    def __unicode__(self):
        return self.text
        
        


        




    

    
