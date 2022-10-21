from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.utils import json
from rest_framework.views import APIView
from quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# Method 1
@api_view(['GET', 'POST'])
def endpoint1(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse('Get_method1')
    if request.method == 'POST':
        return HttpResponse("Post_method2")


# Method 2
class CartItemViews(APIView):
    def get(self, request):
        return HttpResponse('Get_method2')

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content1 = body['Test']
        content2 = body['Test2']
        return HttpResponse([content1, content2])
