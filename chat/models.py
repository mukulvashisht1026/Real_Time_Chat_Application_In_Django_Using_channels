from django.db import models
from django.contrib.auth.models import User
from django.db import models

from django.conf import settings
from django.db import models
from django.db.models import Q


class ThreadManager(models.Manager):
	def get_msg(self,user1,user2):
		messagesThread = self.get_queryset().filter(Q(sender=user1,reciever=user2) | Q(sender=user2,reciever=user1)).order_by('timestamp')
		'''for i in messagesThread:
			print(i," sender ",i.sender,"  timestamp :",i.timestamp)'''
		return messagesThread

	def create(self,msg,sender,reciever):
		obj = self.model(msg=msg,sender=sender,reciever=reciever)
		obj.save()
		return obj
# Create your models here.
'''class messages(models.Model):
	msg =  models.CharField(max_length=1000)
	inbox = models.ForeignKey(User,unique=True)


class Thread(models.Model):
	sending_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='chat_thread_first')
	recieving_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='chat_thread_second')
'''


class messageStore(models.Model):
	msg = models.CharField(max_length=1000,blank=False)
	sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sender')
	reciever = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reciever')
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.msg


	manager=ThreadManager()