from django.contrib.auth import authenticate, login as auth_login, login, update_session_auth_hash

from django.contrib.auth.models import User
from django.db import transaction

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Details
from actions.models import Activity


def register(request):
    users = User.objects.all()
    if request.method == 'POST':
        # Registration logic
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        last_name = request.POST.get('last-name')
        first_name = request.POST.get('first-name')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "users/user/login.html")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "users/user/login.html")
        else:
            # Create a new user
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name  # Set first name
            user.last_name = last_name  # Set last name
            user.save()

            # Authenticate the user and log them in
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,
                                 "You have successfully registered as %s and are now logged in." % user.username)
                return redirect('users:register')
            else:
                messages.error(request, "Invalid credentials")
                return render(request, "users/user/login.html")

    return render(request, "users/user/login.html", {'users': users})


def profile(request, username):
    actions = Activity.objects.all().order_by('-created')[:10]
    user_profile = get_object_or_404(User, username=username)
    context = {
        'user_profile': user_profile,
        'actions': actions,
    }
    return render(request, "users/user/profile.html", context)


def login_user(request):
    request.session.flush()
    if request.method == 'POST':
        username = request.POST.get('login-username')
        password = request.POST.get('login-password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['username'] = user.username
            request.session['role'] = user.details.role
            print("asdasdad"+request.session.get('username'))
            auth_login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('finance:dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "users/user/login.html")


@user_passes_test(lambda u: u.is_superuser)
def change_user_role(request):
    actions = Activity.objects.all().order_by('-created')[:10]
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')

        # Update user role

        user = User.objects.get(id=user_id)
        if new_role == 'admin':
            user.is_superuser = True
            user.is_staff = True  # Generally, superusers are also staff
        else:
            user.is_superuser = False
            user.is_staff = False
        user_details = Details.objects.get(user=user)
        user_details.role = new_role
        user_details.save()
        user.save()
        return redirect('users:user_management')

    users = User.objects.all()
    return render(request, 'users/user/mangeRoles.html', {'users': users})


def user_management(request):
    actions = Activity.objects.all().order_by('-created')[:10]
    all_users = User.objects.all()
    return render(request, 'users/user/mangeRoles.html', {'all_users': all_users, 'actions': actions,})


@login_required
def delete_user_profile(request):
    if request.method == 'POST':
        user = request.user
        try:
            with transaction.atomic():
                # If there are related models with foreign keys to user, handle them here
                # Example: user.profile.delete()

                user.delete()
                messages.success(request, "Your profile has been successfully deleted.")
        except Exception as e:
            # Handle exceptions (logging and user feedback)
            messages.error(request, "An error occurred while deleting your profile.")

        return redirect('users:login_user')  # Redirect to a safe page, e.g., the home page


def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('new-email')
        user.first_name = request.POST.get('first-name')
        user.last_name = request.POST.get('last-name')
        user.is_staff = request.POST.get('roommate-status') == 'True'

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('users:profile', username=user.username)
    else:
        # Handle GET request if necessary
        pass

    return render(request, 'users/user/profile.html')


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Profile deleted successfully.")
        return redirect('users:login_user')

    return redirect('users:login_user', username=request.user.username)
