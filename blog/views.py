from django.shortcuts import render

# Create your views here.


def docpage(request):
    return render(request, "blog/blog.html")