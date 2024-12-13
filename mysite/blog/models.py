from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='food_images/', null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 2)
        return "No ratings yet"

class Rating(models.Model):
    food = models.ForeignKey(Food, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # Values between 1-5
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('food', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.food.name}: {self.rating}"
