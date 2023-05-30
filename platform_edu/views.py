from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
# from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm
# from django.views.generic.edit import CreateView
# from .forms import CreationForm

def home_page(request):
    return render(request, "main.html")

def videochat(request):
    video = """
<div id="metered-frame"></div>
<script src="https://cdn.metered.ca/sdk/frame/1.4.3/sdk-frame.min.js"></script>
<script>
    var frame = new MeteredFrame(); 
    frame.init({
        // This URL will be different. It will be unique based on your appName and roomName
        roomURL: "yourappname.metered.live/tutorial", 
    }, document.getElementById("metered-frame"));
</script>
"""
    return HttpResponse(video)

# def registration(request):
#     return render(request, "registration/signup.html")

# class SignUp(CreateView):
#     form_class = CreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"

def index(request):
    return HttpResponse("Страница приложения EasyEdu.")

def categories(request, catid):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")

def archive(request, year):
    if int(year) < 2020:
        return redirect('home', permanent=True)

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')