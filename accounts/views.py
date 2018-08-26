from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import UserForm


def signup(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(**form.cleaned_data)
			return redirect('base')
	else:
		form = UserForm()
		return render(request,'accounts/signup.html',{'form':form})


# Create your views here.
