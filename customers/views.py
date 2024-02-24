from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout, get_user_model
from django.contrib import messages
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect,  get_object_or_404
from .forms import UserRegistrationForm,UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.utils.encoding import force_str, force_bytes
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView




class UserRegistrationView(FormView):
    template_name = 'customers/user_registration.html'
    form_class = UserRegistrationForm
    
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False  # User is inactive until confirmation
            user.save()

            token = default_token_generator.make_token(user)
            # uid = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # confirm_link = f"http://127.0.0.1:8000/customer/activate/{uid}/{token}/"
            confirm_link = f"http://raft-cart.onrender.com///customer/activate/{uid}/{token}/"
            email_subject = "Account Activation"
            email_body = render_to_string('customers/confirmation_email.html', {'user': user, 'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            messages.success(request, 'Please check your email for confirmation.')
            return render(request, 'customers/user_registration.html')
        return render(request, self.template_name, {'form': form})

class ConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(get_user_model(), pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Your account has been activated successfully. You can login Now")
        else:
            return HttpResponse("Invalid activation link.")

class UserLoginView(LoginView):
    template_name = 'customers/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

def user_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))

    
class UserProfileView(View):
    template_name = 'customers/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f' You Successfully Updated Your Profile Information')
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})


class PassChangeView(View):
    template_name = 'customers/password_change.html'

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Password Updated Successfully')

            # Send email to the user
            mail_subject = 'Password Change Notification'
            message = render_to_string('customers/password_change_message.html', {'user': request.user})
            # message = render_to_string('customers/password_change_message.html', {'user': request.user})
            to_email = request.user.email
            send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
            send_email.attach_alternative(message, "text/html")
            send_email.send()

            update_session_auth_hash(request, form.user)
            return redirect('profile')

        return render(request, self.template_name, {'form': form})