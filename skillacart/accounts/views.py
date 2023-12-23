from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm
from django.contrib import messages


def register_page(request):
    """
    Renders the registration page and handles user registration.
    If the user is already authenticated, redirects to the home page.
    """
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                # Get the username of the newly created user
                user = form.cleaned_data.get('username')
                # Send a success message
                messages.success(request, 'Account was created for ' + user)
                # Redirect to the home page
                return redirect('home')
        else:
            form = CreateUserForm()

        return render(request, 'components/register.html', context={'form': form})


def login_page(request):
    """
    Renders the login page and handles user authentication.
    If the user is already authenticated, redirects to the home page.
    """
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        return render(request, 'components/login.html')


@login_required
def logout_user(request):
    """
    Logs out the current user and redirects them to the login page.
    """
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('home')