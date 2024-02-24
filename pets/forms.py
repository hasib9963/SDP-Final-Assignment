from django import forms
from .models import Pet, Review

class PetForm(forms.ModelForm):
    class Meta: 
        model = Pet
        # fields = '__all__'
        exclude = ['customer', 'adopted_by']
        
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name','Reviews']

