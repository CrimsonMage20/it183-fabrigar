from django.shortcuts import render, get_object_or_404, redirect
from .models import Food, Rating
from .forms import FoodForm, RatingForm, EditFoodForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib.auth.forms import UserCreationForm
from .serializers import FoodSerializer
from rest_framework import viewsets
from django.contrib import messages
from rest_framework.permissions import AllowAny

@login_required
def food_list(request):
    foods = Food.objects.all()
    return render(request, 'foodrating/food_list.html', {'foods': foods})

@login_required
def food_category_list(request):
    foods = Food.objects.all()
    return render(request, 'foodrating/food_category_list.html', {'foods': foods})

@login_required
def foods_by_category(request, category):
    foods = Food.objects.filter(category__iexact=category)
    return render(request, 'foodrating/foods_by_category.html', {
        'foods': foods,
        'category': category
    })

@login_required
def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)
    ratings = food.ratings.all()
    category = food.category 
    user_rating = None
    if request.user.is_authenticated:
        user_rating = ratings.filter(user=request.user).first()
    return render(
        request,
        'foodrating/food_detail.html',
        {
            'food': food,
            'ratings': ratings,
            'user_rating': user_rating,
            'category': category,
        }
    )

@login_required
def food_create(request, category):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.category = category
            food.save()
            return redirect('foods_by_category', category=category)
    else:
        form = FoodForm()
    return render(request, 'foodrating/food_form.html', {
        'form': form,
        'category': category,
    })

@login_required
def food_update(request, pk):
    # Get the food item by primary key
    food = get_object_or_404(Food, pk=pk)
    
    if request.method == 'POST':
        # Bind the form to the POST data and files, linked to the food instance
        form = EditFoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            updated_food = form.save()  # Save the updated food item
            
            # Get the updated category of the food
            category = updated_food.category
            
            # Redirect to the category page
            return redirect('foods_by_category', category=category)
    else:
        # Create a form instance with the current food data
        form = EditFoodForm(instance=food)
    
    # Render the update form
    return render(request, 'foodrating/food_update.html', {'form': form, 'category': food.category})

@login_required
def food_delete(request, pk):
    # Get the food item by primary key
    food = get_object_or_404(Food, pk=pk)
    
    # Store the food's category for redirection after deletion
    category = food.category  

    if request.method == 'POST':
        try:
            # Attempt to delete the food item
            food.delete()
            messages.success(request, "Food item deleted successfully!")
        except Exception as e:
            # Handle any errors during deletion
            messages.error(request, f"An error occurred while deleting the food item: {e}")
        
        # Redirect to the corresponding category page
        return redirect('foods_by_category', category=category)
    else:
        # Handle invalid request methods
        messages.error(request, "Invalid request method!")
    
    # Redirect to the category page as a fallback
    return redirect('foods_by_category', category=category)

@login_required
def rate_food(request, pk):
    food = get_object_or_404(Food, pk=pk)
    user_rating = food.ratings.filter(user=request.user).first()  # Check if the user already rated this food

    if request.method == 'POST':
        # If the user has already rated, update the existing rating
        if user_rating:
            form = RatingForm(request.POST, instance=user_rating)
        else:
            form = RatingForm(request.POST)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.food = food
            rating.user = request.user
            rating.save()
            return redirect('food_detail', pk=pk)
    else:
        # Pre-fill the form if the user has already rated
        form = RatingForm(instance=user_rating)

    return render(request, 'foodrating/rate_food.html', {'form': form, 'food': food})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'foodrating/register.html', {'form': form})

def delete_rating(request, pk):
    rating = get_object_or_404(Rating, pk=pk, user=request.user)
    if request.method == 'POST':
        rating.delete()
        return redirect('food_detail', pk=rating.food.pk)
    return render(request, 'foodrating/delete_rating_confirm.html', {'rating': rating})

class FoodSerializerViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
