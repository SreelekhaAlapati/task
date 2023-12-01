from django_elasticsearch_dsl import(
    Document, fields, Index
)
from flask import Response

from . models import Ipdetails
from elasticsearch import Elasticsearch

PUBLISHER_INDEX =Index('ipdetails')

PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@PUBLISHER_INDEX.doc_type
class NewsDocument(Document):
    id=fields.IntegerField(attr="id")
    ip=fields.TextField(
        fields={
            "raw": {
                "type": 'keyword'
            }
        }
    )
    status =fields.TextField(
        fields={
            "raw":{
                "type": 'keyword'
            }
        }
    )

    class Django(object):
        model= Ipdetails

    # def list(self, request, *args, **kwargs):
    #     ipdetailss = NewsDocument.search().query('match', ip='1.1.1')
    #     statuses = []
    #     ip_details_queryset = ipdetailss.objects.filter(status='PENDING')
    #     #for ip in ipdetailss:
    #     #   statuses.append(ip.status)
    #     # print(ip_details_queryset)
    #     return Response(statuses)
