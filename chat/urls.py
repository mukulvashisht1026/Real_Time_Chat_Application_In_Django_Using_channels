from django.urls import path,include
from .views import *
urlpatterns = [
path('home/',index,name='chatroom_home'),

path('logout/',logout_1,name='logout_1'),
path('inbox/<int:reciever_id>',inbox,name='inbox'),
#path('inbox_re/<int:reciever_id>',inbox_re,name='inbox_re'),

]
