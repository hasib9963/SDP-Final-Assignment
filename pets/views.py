from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import forms
from . import models
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from pets.forms import ReviewForm
from pets.models import Pet
from django.contrib import messages


@method_decorator(login_required, name='dispatch')
class AddPetCreateView(CreateView):
    model = models.Pet
    form_class = forms.PetForm
    template_name = 'add_pet.html'
    success_url = reverse_lazy('add_pet')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        messages.success(self.request, 'Congratulations, Your pet "{}" has ben added successfully.'.format(form.instance.pet_title))
        return super().form_valid(form) 
    

@method_decorator(login_required, name='dispatch')
class EditPetView(UpdateView):
    model = models.Pet
    form_class = forms.PetForm
    template_name = 'add_pet.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('report')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, 'Congratulations, You successfully updated your pet information.')
        return response


@method_decorator(login_required, name='dispatch')
class DeletePetView(DeleteView):
    model = models.Pet
    template_name = 'delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('report')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, 'Congratulations, You successfully Delete One of Your Pet .')
        return response


class DetailPetView(View):
    template_name = 'pet_details.html'

    def get(self, request, *args, **kwargs):
        pet = get_object_or_404(Pet, id=self.kwargs['id'])
        reviews = pet.reviews.all()
        review_form = ReviewForm()
        context = {
            'pet': pet,
            'reviews': reviews,
            'review_form': review_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pet = get_object_or_404(Pet, id=self.kwargs['id'])

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has adopted the pet
            print(f'User ID: {request.user.id}')
            print(f'Adopted by user IDs: {pet.adopted_by.all().values_list("id", flat=True)}')
            if pet.adopted_by.filter(id=request.user.id).exists():
                review_form = ReviewForm(request.POST)

                if review_form.is_valid():
                    new_review = review_form.save(commit=False)
                    new_review.pet = pet
                    new_review.save()
                    messages.success(request, 'Your review has been added.')
                    return redirect('detail_pet', id=pet.id)
                else:
                    # Display form errors for debugging
                    # print(review_form.errors)
                    messages.error(request, 'Failed to add review. Please try again.')

                return redirect('detail_pet', id=pet.id)
            else:
                messages.error(request, 'You need to Adopt the pet first before posting a review.')
        else:
            messages.error(request, 'Please login to Adopt the pet and post reviews.')

        return redirect('detail_pet', id=pet.id)
