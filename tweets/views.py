import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect

from .forms import TweetForm
from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1> Hello world</h1>")
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    print(next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url is not None:
            return redirect(next_url)
        return redirect('/')
    return render(request, 'components/form.html', {"form":form})

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by Javascript
    return json data
    """
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 10101)} for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
        #"content": obj.content,
        # "image_path": obj.image.url
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except Tweet.DoesNotExist:
        data['message'] = "Not found"
        return JsonResponse(data, status=404)
    return JsonResponse(data, status=200)


    return JsonResponse(data, status=status)