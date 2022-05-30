from django.shortcuts import render, redirect
from .models import TweetModel
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    user = request.user.is_authenticated # 로그인이 되어 있는지 확인하는 기능
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})  # {'tweet': all_tweet} 데이터를 화면에 넘겨주겠다.
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        user = request.user  # 사용자의 전체 정보를 불러옴
        my_tweet = TweetModel()
        my_tweet.author = user
        my_tweet.content = request.POST.get('my-content', '')
        my_tweet.save()
        return redirect('/tweet')

# 로그인이 되어 있어야만 실행
@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')