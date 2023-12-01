from .models import Ipdetails
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import *

class NewsDocumentSerializer(DocumentSerializer):
    def get_location(self, obj):
        try:
            return obj.location.to_dict()
        except:
            return {}

    class Meta:
        model = Ipdetails
        document = NewsDocument
        fields = ('ip', 'status')
