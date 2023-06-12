from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import JsonResponse, HttpResponseNotFound
from .models import AccessKey
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import *
from verify_email.email_handler import send_verification_email


@login_required
def home(request):
    return render(request, 'base/home.html', {'section': 'home'})


# register new user
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but aboid saving it yet
            new_user = user_form.save(commit=False)
            # set chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # send verification email to user's email address
            # to activate account
            new_user = send_verification_email(request, user_form)

            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form':user_form})


# access keys
class GenerateAccessKeyView(View):
    def get(self, request):
        form = AccessKeyForm()
        return render(request, 'base/access_key_form.html', {'form': form})

    def post(self, request):
        form = AccessKeyForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            user = form.cleaned_data['user']

            if AccessKey.objects.filter(status='active', user=user).exists():
                error_message = f"An active access key already exists for this user {user}."
                return render(request, 'base/access_key_form.html', {'form': form, 'error_message': error_message})

            access_key = AccessKey(status=status, user=user)
            access_key.save()
            return redirect('access_keys')

        return render(request, 'base/access_key_form.html', {'form': form})
    

class AccessKeyView(View):
    def get(self, request):
        user = request.user

        if user.is_staff:
            access_keys = AccessKey.objects.order_by('status', 'user', 'expiry_date')
        else:
            access_keys = AccessKey.objects.filter(user=request.user).order_by('status', 'expiry_date')
        
        active_keys = access_keys.filter(status='active').count()
        return render(request, 'base/access_keys.html', {'access_keys': access_keys, 'active_keys':active_keys})
    
    
@staff_member_required
@login_required
def admin_dashboard(request):
    access_keys = AccessKey.objects.all()        
    return render(request, 'base/access_keys.html', {'access_keys': access_keys})


@staff_member_required
@login_required
def revoke_access_key(request, pk):
    access_key = AccessKey.objects.get(id=pk)
    if request.method == 'POST':
        access_key.status = 'revoked'
        access_key.save()
        return redirect(reverse('access_keys')) # Redirect to the revoke_key.html page

    context = {'access_key': access_key,}
    return render(request, 'base/revoke_key.html', context)

# endpoint
@staff_member_required
@login_required
def check_school_email(request):
    if request.method == 'GET':
        school_email = request.GET.get('email', '')

        try:
            access_key = AccessKey.objects.get(user__email=school_email, status='active')
            key_details = {
                'key': access_key.access_key,
                'status': access_key.status,
                'procurement_date': access_key.procurement_date,
                'expiry_date': access_key.expiry_date
            }
            return JsonResponse(key_details, status=200)
        except AccessKey.DoesNotExist:
            return HttpResponseNotFound()
        

@staff_member_required
@login_required
def endpoint_view(request):
    return render(request, 'base/endpoint.html')