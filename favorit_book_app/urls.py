from django.urls import path
from . import views

urlpatterns = [
    # Login and Registration
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    # Main Games Dashboard
    path('dashboard', views.games),
    path('games/create', views.create_game),

    # Book Details, Update, and Delete
    path('games/<int:game_id>', views.show_game),
    path('games/<int:game_id>/edit', views.edit_game), #show edit page
    path('games/<int:game_id>/update', views.update_game), #actual editing
    path('games/<int:game_id>/delete', views.delete_game),





    # Favorite Actions
    #path('books/<int:book_id>/favorite', views.favorite),
   # path('books/<int:book_id>/unfavorite', views.unfavorite),

    # SENSEI BONUS: User's Favorites Page
   # path('user/favorites', views.my_favorites),
]