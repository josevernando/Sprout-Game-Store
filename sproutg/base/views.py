from django.shortcuts import render

# Create your views here.
def home(req):
    return render(request=req, template_name='base/home.html')