from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.views import View

from api.response import Response, PageResponse
from api.serializers import GroupSerializer


class GroupListView(View):
    @staticmethod
    def get(request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        response = Response(model=serializer.data,
                            message="List of roles was retrieved successfully")
        return JsonResponse(response.__dict__, status=200)
