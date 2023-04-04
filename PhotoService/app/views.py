from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Photo
from django.contrib.auth.decorators import login_required
from .forms import PhotoForm
from django.contrib import messages
from django.views.decorators.http import require_POST

def index(request):
  return render(request, 'app/index.html')

def users_detail(request, pk):
  user = get_object_or_404(User, pk=pk)
  photos = user.photo_set.all().order_by('-created_at')
  return render(request, 'app/users_detail.html', {'user': user, 'photos':
photos})

def index(request):
  photos = Photo.objects.all().order_by('-created_at')
  return render(request, 'app/index.html', {'photos': photos})

def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      input_username = form.cleaned_data['username']
      input_password = form.cleaned_data['password1']
      # フォームの⼊⼒値で認証できればユーザーオブジェクト、できなければNoneを返す
      new_user = authenticate(
      username=input_username,
      password=input_password,
      )
      # 認証成功時のみ、ユーザーをログインさせる
      if new_user is not None:
      # login関数は、認証ができてなくてもログインさせることができる。(認証は上のauthenticateで実⾏する)
        login(request, new_user)
        return redirect('app:users_detail', pk=new_user.pk)
  else:
    form = UserCreationForm()
  return render(request, 'app/signup.html', {'form': form})

@login_required
def photos_new(request):
  if request.method == "POST":
    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():
      photo = form.save(commit=False) #FalseにすることでDBに保存しないようにしている。この段階ではuserフィールドに入れる値が決まってないためエラーが出る
      photo.user = request.user
      photo.save() #ここで全てのフィールドに値が入った状態になるのでDBに保存できる
      messages.success(request, "投稿が完了しました!")
    return redirect('app:users_detail', pk=request.user.pk)
  else:
    form = PhotoForm()
  return render(request, 'app/photos_new.html', {'form': form})

def photos_detail(request, pk):
  photo = get_object_or_404(Photo, pk=pk)
  return render(request, 'app/photos_detail.html', {'photo': photo})

@require_POST
def photos_delete(request, pk):
  photo = get_object_or_404(Photo, pk=pk, user=request.user)
  photo.delete()
  return redirect('app:users_detail', request.user.id)