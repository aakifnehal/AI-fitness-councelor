from django.shortcuts import render, HttpResponse,redirect
import calculation
import requests
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from datetime import datetime
from Home.models import userData
from .utils import get_plot1,get_plot2

# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect("/signup")
    e=""
    fit=""
    response=""
    Output=""
    try:
        if request.method == "POST":

            w = eval(request.POST.get('weight'))
            #print(w)
            h = eval(request.POST.get('height'))
            #print(h)
            e = w/((h/100)**2)
            #print(e)
            t = eval(request.POST.get('time'))
            print(t)
            if e > 25:
                fit = "overweight"
            elif e < 18:
                fit = "underweigt"
            else:
                fit= "fullyfit"
            text1="gym plan for person with bmi "+str(e)+"and having time of "+str(t)+" minutes"
            print(text1)
            r = requests.post("https://api.deepai.org/api/text-generator",data={'text':text1 ,},headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'})
            response=r.json()
            print(response)
            Output=response.get('output')
            print(Output)
            print(r)
            userdata=userData(userName=request.user,weight=w,hieght=h,bmi=e,date=datetime.today())
            userdata.save()
            

    except:

         e="invalid"



    

    context={'e':e,'fit':fit,'plan':Output}
    return render(request, 'index.html',context)
    #return HttpResponse("this is home page")


def loginUser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
            return redirect("/")
        else:
            # No backend authenticated the credentials
            return render(request,"login.html")
    return render(request,"login.html")

def logoutUser(request):
    logout(request)
    # Redirect to a success page.
    return redirect("/login")

def signupUser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        login(request,user)
        return redirect("/")
    return render(request,"login.html")

def statistics(request):
    qs=userData.objects.filter(userName=request.user)
    x1 = [x.date for x in qs]
    y1 = [y.bmi for y in qs]
    z = [y.weight for y in qs]
    chart1 = get_plot1(x1, y1)

    chart2=get_plot2(x1,z)
    return render(request,"stats.html",{'chart1':chart1,'chart2':chart2})