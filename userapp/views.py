import json
import celery
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from . import tasks
from . models import Ipdetails
from celery.result import AsyncResult
from elasticsearch_dsl import Q
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from . documents import *
from . serializers import *
from django_elasticsearch_dsl_drf.filter_backends import(
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
)

# Create your views here.
def home(request):
    return render(request,"home.html")
def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            # return HttpResponse('<h1>Logged in</h1>')
            auth.login(request,user)
            #return HttpResponse('<h1>Logged in</h1>')
            return redirect("/")
        else:
            messages.info(request,"Invalid credentials")
            return redirect('login')
    else:
        return render(request,"login.html")

def register(request):
    if request.method=="POST":
        print("here")
        username=request.POST["username"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists")
                return redirect("register")
            else:
                user=User.objects.create_user(username=username,password=password1)
                user.save()
                print("user saved")
                return redirect('/login')
        else:
            messages.info(request,"Passwords don't match")
            return redirect("register")
    else:
        return render(request,"register.html")

def usersdisp(request):
    user= User.objects.all()
    return render(request,'users.html',{'users':user,'check':True})


def usersdisplay(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users.html', {'user': user})

def some_view(request):
    if request.method=="POST":
        #ip_address = request.POST["ip"]
        # search = Ipdetails.search(using='default', index=index_name).query('match', ip=ip_address)
        # response = search.execute()
        # if not response.hits:
            #(or)
        if not Ipdetails.objects.filter(ip=request.POST["ip"]).exists():
            ip_address = request.POST["ip"]
            print(ip_address)
            task_result = Ipdetails.objects.create(
                ip=ip_address,
                status="PENDING"
            )
            task_result.save()
            response=tasks.get_virustotal_data.delay(ip_address)
            print(response)
            result = AsyncResult(response)
            while not result.ready():
                pass
            if result.ready():
                print(result.get())
                json_string = json.dumps(result.get())
                task_result = result.get()
                print(task_result)
                if json_string[2]=='e':
                    status="ERROR"
                else:
                    status="SUCCESS"
            else:
                status="PENDING"
            try:
                task_result = Ipdetails.objects.get(ip=ip_address)
                task_result.status = status
                task_result.save()
                print("DATA IS SAVED")
            except Ipdetails.DoesNotExist:
                pass
            return HttpResponse(task_result)
        else:
            return HttpResponse(Ipdetails.objects.filter(request.POST["ip"]).status)
    else:
        return render(request,"ipadress.html")
    

def enrichip(request, ip):
    try:
        ip_details = Ipdetails.objects.get(ip=ip)
        status = ip_details.status
        return HttpResponse(status)
    except Ipdetails.DoesNotExist:
        ip_address = ip
        response = tasks.get_virustotal_data(ip_address)
        result=json.dumps(response)
        print(response)
        if result[2]=='d':
            task_result = Ipdetails.objects.create(
                ip=ip_address,
                status="SUCCESS"
            )
            task_result.save()
            return HttpResponse("SUCCESS")
        else:
            task_result = Ipdetails.objects.create(
                ip=ip_address,
                status="ERROR"
            )
            return HttpResponse("ERROR")
        

def ipdisp(request):
    ipdetails= Ipdetails.objects.all()
    return render(request,'ipdisp.html',{'ipdetails':ipdetails,'check':True})

class PublisherDocumentView(DocumentViewSet):
    document = NewsDocument
    serializer_class = NewsDocumentSerializer
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend
    ]
    search_fields = (
        'ip',
        'status'
    )
    multi_match_search_fields = ('ip', 'status')

    fields_fields = {
        'ip': 'ip',
        'status': 'status'
    }

from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class StatusSuccessAPIView(APIView):
    def get(self, request, query):
        base_url = 'http://localhost:9200'
        index_name = 'ipdetails'

        # Use double quotes for the entire f-string and single quotes for query parameters
        search_endpoint = f"{base_url}/{index_name}/_search?q={query}"

        try:
            response = requests.get(search_endpoint)
            if response.status_code == 200:
                data = response.json().get('hits', {}).get('hits', [])
                results = [
                    {'id': hit['_id'], 'ip': hit['_source']['ip'], 'status': hit['_source']['status']}
                    for hit in data
                ]
                return Response(results)
            else:
                return Response({'message': 'Search failed'}, status=response.status_code)
        except requests.RequestException as e:
            return Response({'message': f'Error: {e}'}, status=500)
