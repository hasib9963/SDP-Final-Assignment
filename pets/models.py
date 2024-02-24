from django.db import models
from categories.models import Category
from django.contrib.auth.models import User


class Pet(models.Model):
    pet_title = models.CharField(max_length=50)
    description = models.TextField()
    price =models.DecimalField(decimal_places=2, max_digits = 12)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    adopted_by = models.ManyToManyField(User, related_name='adopted_pet', blank=True)
    images = models.ImageField(upload_to='pets/media/uploads/')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.pet_title
    
class Review(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    Reviews = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Reviews by {self.name}"
