from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book
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
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
    request.session['user_id'] = user.id
    return redirect('/books')

def login(request):
    user = User.objects.filter(email=request.POST['email']).first()
    if user and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        return redirect('/books')
    messages.error(request, "Invalid credentials")
    return redirect('/')

# --- BOOK DASHBOARD ---
def books(request):
    if 'user_id' not in request.session: return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_books": Book.objects.all()
    }
    return render(request, "books.html", context)

def create_book(request):
    errors = Book.objects.book_validator(request.POST)
    if errors:
        for val in errors.values(): messages.error(request, val)
        return redirect('/books')
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], uploaded_by=user)
    # Automatically favorite on upload
    book.users_who_like.add(user)
    return redirect('/books')

def show_book(request, book_id):
    if 'user_id' not in request.session: return redirect('/')
    context = {
        "book": Book.objects.get(id=book_id),
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "show_book.html", context)

# --- ACTIONS ---
def update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.title = request.POST['title']
    book.desc = request.POST['desc']
    book.save()
    return redirect(f'/books/{book_id}')

def delete_book(request, book_id):
    Book.objects.get(id=book_id).delete()
    return redirect('/books')

def favorite(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    Book.objects.get(id=book_id).users_who_like.add(user)
    return redirect(request.META.get('HTTP_REFERER', '/books'))

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    Book.objects.get(id=book_id).users_who_like.remove(user)
    return redirect(request.META.get('HTTP_REFERER', '/books'))

def logout(request):
    request.session.flush()
    return redirect('/')

# SENSEI BONUS: My Favorites Page
def my_favorites(request):
    if 'user_id' not in request.session: return redirect('/')
    context = { "user": User.objects.get(id=request.session['user_id']) }
    return render(request, "my_favorites.html", context)