from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import CreateView
from .form import PatientSignUpForm, DoctorSignUpForm, UserUpdateForm, PatientProfileUpdateForm, DoctorProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
#new for activation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token


def register(request):
    return render(request, '../templates/accounts/register.html')

class patient_register(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = '../templates/accounts/patient_register.html'

    def form_valid(self, form):
        user = form.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('accounts/emails/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)

        messages.success(self.request, ('Please Confirm your email to complete registration.'))
        return redirect('accounts:confirm')
        # login(self.request, user)
        # return redirect('/')
        # return render('accounts/confirm.html')



#new import for second activation
from .tokens import account_activation_token2

#new modification to messages
from django.contrib import messages as messages2

class doctor_register(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = '../templates/accounts/doctor_register.html'

    #formerly used without email activation
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('/')

    def form_valid(self, form):
        user = form.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your MySite Account - Doctor'
        message = render_to_string('accounts/emails/account_activation2_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token2.make_token(user),
        })
        user.email_user(subject, message)

        messages.success(self.request, ('Please Confirm your email to complete registration.'))
        return redirect('accounts:confirm')
        # return render('accounts/confirm.html')
        # return redirect('login')
        # login(self.request, user)
        # return HttpResponse("<h1>Thank you for signing-up with us. Kindly check your email to activate</h1>")

def confirm(request):
    context = {
    }
    return render(request, 'accounts/confirm.html', context)


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = authenticate(username=User.objects.get(email=username), password=password)
            except User.DoesNotExist:
                user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/accounts/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    messages.success(request, 'Thank you, Hope to see you soon')
    # return redirect('/')
    return render(request, 'accounts/logout.html')
# 'accounts/logoutin.html'

#--------------------------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from .decorators import *

#profile new
@patient_only
def patient_profile(request):
    # if not request.user.is_customer == True:
    #     return HttpResponseRedirect(reverse('employee-profile'))
    # Role.ADMIN
    # if not request.user.roles == Role.PATIENT:
    #     return HttpResponseRedirect(reverse('doctor-profile'))

    context = {
    }
    return render(request, 'accounts/user/profile.html', context)

#profile_employee/staff - newest
@doctor_only
def doctor_profile(request):
    #new decorator added
    # if not request.user.is_employee == True:
    #     return HttpResponseRedirect(reverse('user-profile'))
    # if request.user.roles != Role.INT_DOCTOR:
    #     return HttpResponseRedirect(reverse('user-profile'))

    context = {
    }
    return render(request, 'accounts/user/profile2.html', context)


@patient_only
def profile_update(request):
    #Only customer can acess -  working , nevertheless will use decorators
    # if not request.user.is_customer == True:
    # if request.user.roles != 1:
    #     return HttpResponseRedirect(reverse('doctor-profile-update'))

    if request.method == 'POST':
        #the reason the form was not saving was because i didnot request files when i changed
        #i.e when the image file field from p_form to u_form
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form = PatientProfileUpdateForm(
            request.POST, instance=request.user.patient)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('accounts:user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PatientProfileUpdateForm(instance=request.user.patient)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/user/profile_update.html', context)

# newwwwwww
@doctor_only
def doctor_profile_update(request):
    # if not request.user.roles == 2:
    #     return HttpResponseRedirect(reverse('user-profile-update'))

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form = DoctorProfileUpdateForm(
            request.POST, instance=request.user.doctor)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('accounts:doctor-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = DoctorProfileUpdateForm(instance=request.user.doctor)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/user/profile2_update.html', context)

#new
from django.views.generic import View, UpdateView
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if not user.patient.email_confirmed == True:
                user.is_active = True
                user.patient.email_confirmed = True
                user.save()
                #new seg - saving profile now
                user.patient.save()
                login(request, user)
                messages.success(request, ('Your account have been confirmed.'))
                return redirect('/')
            else:
                return HttpResponse("<h1>Email Previously activated. Kindly login with your username and password </h1>")
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/')


########################
#2ND ACTIVATION

class ActivateAccountDoctor(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token2.check_token(user, token):
            user.is_active = True
            user.doctor.email_confirmed = True
            user.save()
            user.doctor.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('/')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/')




# ----------scammmmmm test----------------
def login_request123(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = authenticate(username=User.objects.get(email=username), password=password)
            except User.DoesNotExist:
                user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'accounts/login.html',
    context={'form':AuthenticationForm()})