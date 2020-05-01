from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def ss(request):
    return render(request, 'users/authentification/login.html')


def monitoring(request):
    return render(request,'pagedccueille.html',{'title':'Network Monitoring and anomalys detection system'})




@login_required
def profile(request):
    return render(request, 'users/authentification/profile.html')