from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from trendz.forms import Loginform, Registerform, Inputform
from .models import User, Data, Param 
from django.db import IntegrityError
from django.views.generic import TemplateView
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.
@csrf_exempt
def index(request):
    
    if request.user.is_authenticated and request.method == "GET": 
        user = User.objects.get(username=request.user.username)
        form = Inputform()
        record = Data.objects.filter(user=user).order_by("-date")

        return render(request, "trendz/index.html", {
                "user" : user,
                "form" : form.as_p(),
                "record" : record, 
                
            })

    elif request.user.is_authenticated and request.method == "POST":
        user = User.objects.get(username=request.user.username)
        form = Inputform(request.POST)
        if form.is_valid():
            fs = form.cleaned_data["fs"]
            pp = form.cleaned_data["pp"]
            hba1c = form.cleaned_data["hba1c"]
            hb = form.cleaned_data["hb"]
            rbc = form.cleaned_data["rbc"]
            wbc = form.cleaned_data["wbc"]
            pl = form.cleaned_data["pl"]
            cr = form.cleaned_data["cr"]
            date = form.cleaned_data["date"]
            if fs or pp or hb or hba1c or hb or rbc or wbc or pl or cr is not None:
                record = Data.objects.create(user=user, fs=fs, pp=pp, hba1c=hba1c, hb=hb, rbc=rbc, wbc=wbc, pl=pl, cr=cr, date=date)
                messages.add_message(request, messages.INFO, 'Record saved successfully!')
                return HttpResponseRedirect(reverse("index"))

            else:
                record = Data.objects.filter(user=user).order_by("-date")
                return render(request, "trendz/index.html", {
                    "message" : "Please enter atleast one of the parameters below.",
                    "form" : form.as_p(),
                    "record": record,
                })

    if request.user.is_authenticated and request.method == "PUT": 
        user = User.objects.get(username=request.user.username)
        form = Inputform()
    
        return render(request, "trendz/index.html", {
                "user" : user,
                "form" : form.as_p(),
                "message" : "Record deleted."
                
            })

    else:
        form = Inputform()
        return render(request, "trendz/index.html", {
            "form": form.as_p(),
            "message" : "Please Log in or Register if first time user",

        })


def login_view(request):
    if request.method == "POST":
        # If request is POST, create a form instance and populate it with data from the request:
        form = Loginform(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required    
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
             
            user = authenticate(request, username=username, password=password)
           
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "trendz/index.html", {
                    "message": "Incorrect username/password."
                    })    
        else:
            render(request, "trendz/login.html",{
                "message" : "Please enter valid data",
                })
        
    else:
        form = Loginform()
        return render(request, 'trendz/login.html', {
            'form': form.as_p(),
            
            })



def register(request):
    if request.method == "POST":
        # If request is POST, create a form instance and populate it with data from the request:
        form = Registerform(request.POST)
       
        # Check if the form is valid:
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Ensure password matches confirmation
            confirmation = form.cleaned_data["confirmation"]
            if password != confirmation:
                return render(request, "trendz/register.html", {
                "message" : "Password must match.",
            })
       
            # Attempt to create new user
            try:
                user = User.objects.create_user(username, password=password)
                user.save()
                
            except IntegrityError:
                return render(request, "trendz/register.html", {
                    "message" : "Username already taken.",
                     "form": form.as_p(),
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:

            return render(request, "trendz/register.html",{
                "message" : "Please enter valid data",
                "form" : form.as_p(),
            })

    else:
        
        form = Registerform()
        return render(request, "trendz/register.html", {
            "form": form.as_p(),
        })



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def chart(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        record = Data.objects.filter(user=user).order_by("-date")
        return JsonResponse([rec.serialize() for rec in record], safe=False)


def normalval(request):
    if request.user.is_authenticated:       
        nv = Param.objects.all()
        return JsonResponse([n.serialize() for n in nv], safe=False)


@csrf_exempt
def deleterecord(request):
 
    if request.user.is_authenticated and request.method == "PUT":
        user = User.objects.get(username=request.user.username)
    
        data = json.loads(request.body)
        if data.get("rowid") != [] :
            rows_d = data.get("rowid")
            for r in rows_d:
                Data.objects.filter(id=r,user=user).delete()
            
            return JsonResponse({"message": "Record deleted successfully"}, safe=False)
            
                
        
        else:
            data = json.loads(request.body)
            rows_d = data.get("rowid")
            
            return JsonResponse({"message": "Select rows to delete"}, safe=False)
            
            
    