from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Game
import bcrypt

# --- LOGIN & REG ---
def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if errors:
        for val in errors.values(): messages.error(request, val)
        return redirect('/')
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        date_of_birth=request.POST['date_of_birth'],
        password=pw_hash)
    request.session['user_id'] = user.id
    return redirect('/dashboard')

def login(request):
    user = User.objects.filter(email=request.POST['email']).first()
    if user and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        return redirect('/dashboard')
    messages.error(request, "Invalid credentials")
    return redirect('/')

# --- Game DASHBOARD ---
def games(request):
    if 'user_id' not in request.session: return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_games": Game.objects.all()
    }
    return render(request, "games.html", context)

def create_game(request):
    errors = Game.objects.game_validator(request.POST)
    if errors:
        for val in errors.values(): messages.error(request, val)
        return redirect('/dashboard')
    user = User.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        Game.objects.create(
        name=request.POST['name'],
        genre=request.POST['genre'],
        release_date=request.POST['release_date'],
        desc=request.POST['desc'],
        created_by=user
        )
    return redirect('/dashboard')

def show_game(request, game_id):
    if 'user_id' not in request.session: return redirect('/')
    game = Game.objects.get(id=game_id)
    user = User.objects.get(id=request.session['user_id'])
    show_button = user==game.created_by
    context = {
        "game": Game.objects.get(id=game_id),
        "user": User.objects.get(id=request.session['user_id']),
        'show_button': show_button
    }
    return render(request, "show_game.html", context)

def edit_game (request,game_id):
    if 'user_id' not in request.session: return redirect('/')
    context = {
        "game": Game.objects.get(id=game_id),
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "edit_game.html", context)  


# --- ACTIONS ---
def update_game(request, game_id):
    errors = Game.objects.game_validator(request.POST)
    if errors:
        for val in errors.values(): messages.error(request, val)
        return redirect(f'/games/{game_id}/edit')
    if request.method=='POST':
        game = Game.objects.get(id=game_id)
        game.name=request.POST['name']
        game.genre=request.POST['genre']
        game.release_date=request.POST['release_date']
        game.desc=request.POST['desc']
        game.save()
    return redirect(f'/games/{game_id}')

def delete_game(request, game_id):
    Game.objects.get(id=game_id).delete()
    return redirect('/dashboard')


def logout(request):
    request.session.flush()
    return redirect('/')






#def favorite(request, book_id):
#    user = User.objects.get(id=request.session['user_id'])
#    Book.objects.get(id=book_id).users_who_like.add(user)
#   return redirect(request.META.get('HTTP_REFERER', '/books'))

#def unfavorite(request, book_id):
#    user = User.objects.get(id=request.session['user_id'])
#    Book.objects.get(id=book_id).users_who_like.remove(user)
#    return redirect(request.META.get('HTTP_REFERER', '/books'))



# SENSEI BONUS: My Favorites Page
#def my_favorites(request):
#    if 'user_id' not in request.session: return redirect('/')
#    context = { "user": User.objects.get(id=request.session['user_id']) }
#   return render(request, "my_favorites.html", context)