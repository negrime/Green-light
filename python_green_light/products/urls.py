from django.urls import path,include
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<int:product_id>', views.detail, name='detail'),
    path('<int:product_id>/upvote', views.upvote, name='upvote'),
    path('<int:product_id>/downvote', views.downvote, name='downvote'),
    path('profile', views.profile, name="profile"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('edit/<int:id>/', views.edit, name="edit")

]
