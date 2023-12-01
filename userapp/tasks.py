import json
from celery import shared_task
import requests
from celery import shared_task
from . models import Ipdetails

@shared_task
def add(a,b):
    return a+b

@shared_task
def get_virustotal_data(ip):
    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
    headers = {
        "accept": "application/json",
        "x-apikey": "a0a9a1ca3373773c9bf96d9ce87471960e3510b51ac5f6aa245406104a74a770"
    }
    response = requests.get(url, headers=headers)
    result_data = response.json()
    # instance = Ipdetails.objects.get(ip=ip)
    # json_string = json.dumps(result_data)
    # if json_string[2]=='e':
    #    status="ERROR"
    # else:
    #    status="SUCCESS"
    # instance.status = status
    # instance.save()
    return result_data