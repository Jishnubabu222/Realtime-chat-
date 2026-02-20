from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Message
from django.db.models import Q
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'register.html')

        user = CustomUser.objects.create_user(email=email, username=username, password=password)
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            user.is_online = True
            user.save()
            return redirect('users')
        else:
            messages.error(request, "Invalid email or password!")

    return render(request, 'login.html')

def logout_user(request):
    user = request.user
    if user.is_authenticated:
        user.is_online = False
        user.save()
    logout(request)
    return redirect('login')

from django.db.models import Q, Count

@login_required(login_url='login')
def user_list(request):
    # Annotate each user with the count of unread messages sent TO the current user
    users = CustomUser.objects.exclude(id=request.user.id).annotate(
        unread_count=Count(
            'sent_messages',
            filter=Q(receiver=request.user, is_read=False)
        )
    )
    return render(request, 'user_list.html', {'users': users})

@login_required(login_url='login')
def chat_view(request, user_id):
    receiver = get_object_or_404(CustomUser, id=user_id)
    sender = request.user

    # Mark messages as read
    Message.objects.filter(sender=receiver, receiver=sender, is_read=False).update(is_read=True)

    messages_list = Message.objects.filter(
        (Q(sender=sender) & Q(receiver=receiver)) | 
        (Q(sender=receiver) & Q(receiver=sender))
    ).order_by('timestamp')

    # Get all users for the sidebar with unread counts
    users = CustomUser.objects.exclude(id=request.user.id).annotate(
        unread_count=Count(
            'sent_messages',
            filter=Q(receiver=request.user, is_read=False)
        )
    )

    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages_list': messages_list,
        'users': users
    })
