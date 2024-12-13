from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.food_category_list, name='food_category_list'),
    path('food/<int:pk>/', views.food_detail, name='food_detail'),
    path('food/create/<str:category>/', views.food_create, name='food_create'),
    path('food/<int:pk>/update/', views.food_update, name='food_update'),
    path('food/<int:pk>/delete/', views.food_delete, name='food_delete'),
    path('food/<int:pk>/rate/', views.rate_food, name='rate_food'),
    path('login/', auth_views.LoginView.as_view(template_name='foodrating/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='food_category_list'), name='logout'),
    path('register/', views.register, name='register'),
    path('rating/<int:pk>/delete/', views.delete_rating, name='delete_rating'),
    path('api/', include('blog.api_urls')),
    path('categories/<str:category>/', views.foods_by_category, name='foods_by_category')
]
