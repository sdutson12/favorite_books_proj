from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from .models import User, Book
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['userid'] = user.id
        request.session['name'] = user.first_name
        return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            print(logged_user.first_name)
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                request.session['first_name'] = logged_user.first_name
                request.session['last_name'] = logged_user.last_name
                print("-------------------------------")
                print(request.session['userid'])
                print(request.session['first_name'])
                print(request.session['last_name'])
                print("-------------------------------")
                return redirect('/dashboard')
            else:
                return HttpResponse('Incorrect Password')

def dashboard(request):
    context = {
        'books' : Book.objects.all(),
        'current_user' : User.objects.get(id=request.session['userid']) 
    }
    try:
        if request.session['userid']:
            print(request.session['userid'])
    except:
        return redirect('/')
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def create_book(request):
    errors = Book.objects.new_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        user = User.objects.get(id=request.session['userid'])
        new_book = Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], uploaded_by=user)
        new_book.users_who_like.add(user)
        return redirect('/dashboard')

def show(request, req_id):
    context = {
        'book' : Book.objects.get(id=req_id),
        'current_user' : User.objects.get(id=request.session['userid'])
    }
    return render(request, 'show.html', context)
def remove_from_favs(request, req_id):
    book = Book.objects.get(id=req_id)
    user = User.objects.get(id=request.session['userid'])
    book.users_who_like.remove(user)
    return redirect(f"/show/{book.id}")

def add_to_favs(request, req_id):
    book = Book.objects.get(id=req_id)
    user = User.objects.get(id=request.session['userid'])
    book.users_who_like.add(user)
    return redirect(f"/show/{book.id}")

def edit(request, req_id):
    context = {
        'book' : Book.objects.get(id=req_id)
    }
    return render(request, 'edit.html', context)

def update(request):
    book = Book.objects.get(id=request.POST['book_id'])
    errors = Book.objects.new_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/edit/{book.id}")
    else:
        book.title = request.POST['title']
        book.desc = request.POST['desc']
        book.save()
        return redirect(f"/show/{book.id}")

def destroy(request, req_id):
    book = Book.objects.get(id=req_id)
    book.delete()
    return redirect('/dashboard')