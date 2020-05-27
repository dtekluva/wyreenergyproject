from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from useraccounts.forms import LoginForm
from django.contrib.auth.models import User
# from useraccounts.models import UserAccount, Token_man, Session
from main.models import *
from main import views
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
# from snippet import helpers
import ast


def login_view(request):

        if request.method == 'POST':
                # form = LoginForm(request.POST)

                if True:

                        email    = request.POST.get("email", "")
                        username = request.POST.get("username", "").lower()
                        email = email.lower()
                        password    = request.POST.get("password", "")

                        try:
                                #GET CORRESPONDING USERNAME FROM EMAIL POSTED
                                # username = User.objects.get(email = email).username
                                # user = User.objects.get(username=username)
                                user = authenticate(username = username.lower(), password = password)

                                if (user.username == username): #allows user to login using username
                                        # No backend authenticated the credentials

                                        user = User.objects.get(username=username)
                                        login(request, user)

                                        return HttpResponse(json.dumps({"response":"success"}))
                        except:
                                return HttpResponse(json.dumps({"response":"failure"}))    
                                # return render(request, 'resolute/registration/login.html', {'form' : form, 'error':'Sorry incorrect Username or Password !!!'})
                else:
                        return HttpResponse(json.dumps({"response":"failure"}))    
                        # return render(request, 'resolute/registration/login.html', {'form' : form, 'error':'Sorry incorrect Username or Password !!!'})


        else:
                return render(request, "login.html")

def login_as_view(request, id):

        # form = LoginForm(request.POST)

        if True:

                
                #GET CORRESPONDING USERNAME FROM EMAIL POSTED
                customer = Customer.objects.get(id = id)

                user = customer.user
                login(request, user)

                # return HttpResponse(json.dumps({"response":"success"}))
                
                return redirect(views.index)

                # except:
                #         return HttpResponse(json.dumps({"response":"failure"}))    
                #         # return render(request, 'resolute/registration/login.html', {'form' : form, 'error':'Sorry incorrect Username or Password !!!'})
        else:
                return HttpResponse(json.dumps({"response":"failure"}))    
                # return render(request, 'resolute/registration/login.html', {'form' : form, 'error':'Sorry incorrect Username or Password !!!'})



def update_password(request):

        user = User.objects.get(pk = request.user.id)

        if request.method == 'POST':
                # # print(request.POST)
                old = request.POST.get("old")
                new = request.POST.get("new")
                customer_id = request.POST.get("customer_id", False)
                
                if customer_id == False:

                        user = authenticate(username = user.username, password = old)

                        if user:
                                user.set_password(new)
                                user.save()
                                login(request, user)

                                return HttpResponse(json.dumps({"response": "success"}))
                        else:
                                return HttpResponse(json.dumps({"response": "failure"}))
                else:
                        customer = Customer.objects.get(id = customer_id)
                        # print(customer)
                        # print(customer.user.username)
                        user = authenticate(username = customer.user.username, password = old)
                        # print("----------------------------")

                        if user:
                                user.set_password(new)
                                user.save()

                                return HttpResponse(json.dumps({"response": "success"}))
                        else:
                                return HttpResponse(json.dumps({"response": "failure"}))
