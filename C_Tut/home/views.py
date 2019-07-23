from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'home/homepage.html')
def about(request):
    return render(request,'home/about.html')
def team(request):
    return render(request,'home/team.html')