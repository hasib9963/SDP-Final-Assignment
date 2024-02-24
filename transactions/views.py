from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Adopt
from django.http import HttpResponseRedirect
from .models import Transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from transactions.constants import DEPOSIT
from transactions.forms import DepositForm
from pets.models import Pet



class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('deposit_money')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'
    # success_url = '/transactions/deposit/'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ is deposited to your account successfully'
        )
        mail_subject = 'Deposit Message'
        message = render_to_string('transactions/deposite_email.html', {
            'user' : self.request.user,
            'amount': amount     
        })
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        return super().form_valid(form)



class AdoptPetView(View):
    def post(self, request, *args, **kwargs):
        pet_id = self.kwargs.get('pet_id')
        pet = get_object_or_404(Pet, id=pet_id)
        user_account = request.user.account

        # Check if the user has sufficient balance
        if user_account.balance < pet.price:
            messages.error(request, 'You don\'t have sufficient balance to adopt this pet')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # Create a Borrow instance
        adopt_price = pet.price
        Adopt.objects.create(user_account=user_account, pet=pet, quantity=1, adopt_price=adopt_price)

        # Deduct the book price from the user's account
        user_account.balance -= adopt_price
        user_account.save()

        # Update the book quantity
        pet.quantity -= 1
        pet.save()
        pet.adopted_by.add(request.user)
        # Send email to the user
        mail_subject = 'Adopt Pet'
        message = render_to_string('transactions/adopt_email.html', {
            'user': request.user,
            'pet_title': pet.pet_title,
        })
        to_email = request.user.email
        send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

        # Add success message
        messages.success(request, f' You Successfully Adopt "{pet.pet_title}"')
        
        # Redirect to the same page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



class PetReportView(View):
    def get(self, request, *args, **kwargs):
        user_account = request.user.account
        adopted_pets = Adopt.objects.filter(user_account=user_account)
        data = Pet.objects.filter(customer = request.user)
        return render(request, 'transactions/report.html', {'adopted_pets': adopted_pets, 'data' : data})
