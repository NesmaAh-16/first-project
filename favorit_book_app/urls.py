from django.urls import path
from . import views

urlpatterns = [
    # Login and Registration
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    # Main Books Dashboard
    path('books', views.books),
    path('books/create', views.create_book),

    # Book Details, Update, and Delete
    path('books/<int:book_id>', views.show_book),
    path('books/<int:book_id>/update', views.update_book),
    path('books/<int:book_id>/delete', views.delete_book),

    # Favorite Actions
    path('books/<int:book_id>/favorite', views.favorite),
    path('books/<int:book_id>/unfavorite', views.unfavorite),

    # SENSEI BONUS: User's Favorites Page
    path('user/favorites', views.my_favorites),
]