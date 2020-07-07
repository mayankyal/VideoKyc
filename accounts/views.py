from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import CreateUserForm
from .decorators import *

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='normalUsers')
			user.groups.add(group)
			
			Details.objects.create(
				user=user,
			)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')



@login_required(login_url='login')
def home(request):
	group = None
	if request.user.groups.exists():
		group = request.user.groups.all()[0].name

	if group == 'normalUsers':
		return redirect('userPage')

	if group == 'admin':
		return redirect('adminPage')
	

	

@login_required(login_url='login')
@allowed_users(allowed_roles=['normalUsers'])
def userPage(request):
	context={'user': request.user}
	return render(request, 'accounts/userHome.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminPage(request):
    context={}
    return render(request,'accounts/adminHome.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'normalUsers'])
def room(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	return(render(request , 'accounts/room.html', {'user':user}))


