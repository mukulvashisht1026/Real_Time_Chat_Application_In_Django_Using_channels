import asyncio
import json
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import messageStore



class ChatConsumer(AsyncConsumer):
	other_user=12
	async def websocket_connect(self,event):
		print("connected successfully",event)
		
		other_user_id = self.scope['url_route']['kwargs']['reciever_id']
		self.other_user=other_user_id
		#await asyncio.sleep(10)
		me = self.scope['user']
		print(other_user_id,me)
		current_user=User.objects.get(username=me)
		user_id = current_user.id
		total = other_user_id+user_id
		#obj = await self.get_messages(user_id,other_user_id)
		#print("messages is mukul mayank",obj)
		chat_room = f"room_{total}"
		self.chat_room = chat_room
		await self.channel_layer.group_add(
			chat_room,
			self.channel_name
			)	

		await self.send({
			"type":"websocket.accept"
			})

	async def websocket_receive (self,event):
		print("recieve something",event)
		#recieve something {'type': 'websocket.receive', 'text': '{"message":"madara uchiha"}'}
		front_text = event.get('text',None)
		if front_text is not None:
			loaded_dict_data = json.loads(front_text)
			msg = loaded_dict_data.get('message')
			print(msg)
			user = self.scope['user']
			username = 'default'
			if user.is_authenticated:
				username = user.username
			myResponse ={
			'message':msg,
			'username':username
			}
			#saveing to database

			#me = self.scope['user']
			#current_user=User.objects.get(username=me)
			
			#user_id = current_user.id
			other_user_id = self.scope['url_route']['kwargs']['reciever_id']
			reciever_ins = User.objects.get(id=other_user_id)
			await self.create_chat_message(msg,reciever_ins,user)
			# broadcast the message
			await self.channel_layer.group_send(
				self.chat_room,
				{
				"type":"chat_message",
				"text":json.dumps(myResponse)
				}
			)
			#await self.send()
	async def chat_message(self,event):
		# this sends the actual message
		await self.send({
			"type": "websocket.send",
			"text": event['text']
			})



	async def websocket_disconnect(self,event):
		print("disconnected successfully",event)

	@database_sync_to_async
	def get_messages(self,user_id,other_user):
		return messageStore.manager.get_msg(user_id,other_user).last()


	@database_sync_to_async
	def create_chat_message(self,msg,sender,reciever):
		return  messageStore.manager.create(msg=msg,sender=sender,reciever=reciever)