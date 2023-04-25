
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer

# Create your views here.
class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"massage":"가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"massage":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followers.all():
            you.followers.remove(me)
            return Response("unfollow했습니다.", status=status.HTTP_200_OK)

        else:
            you.followers.add(me)
            return Response("follow했습니다.", status=status.HTTP_200_OK)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class mockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # print(request.user)
        user = request.user
        user.is_admin = True
        user.save()
        return Response('get 요청')
