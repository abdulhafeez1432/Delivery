from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from app.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser, IsCustomerUser, IsOwner
from app.models import *
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
import random
import string
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt




def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))



# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })





class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user





class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ProfileCustomer.objects.all()
    serializer_class = ProfileCustomerSerializer
    permission_classes = (IsOwner,)

    # Ensure a user sees only own The Profile.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ProfileCustomer.objects.filter(user=user)
        raise PermissionDenied()
        
 
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        #email send_email


class CategoryDetailsAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailsSerializer
    permission_classes = (IsAuthenticated,)





@api_view(['GET', 'POST'])
def category_view(request):
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategoryListPageSerializer(category, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategoryListPageSerializer(data=request.data)
        if serializer.is_valid():
            Category.objects.create(**serializer.validated_data)
            return HttpResponse("Category Created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def category_detail_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'GET':
        serializer = CategoryDetailsSerializer(category)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        raise NotImplementedError("PATCH currently not supported")
    elif request.method == 'DELETE':
        raise NotImplementedError("DELETE currently not supported")


@api_view(['GET', 'PATCH', 'DELETE'])
def subcategory_detail_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'GET':
        serializer = SubCategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        raise NotImplementedError("PATCH currently not supported")
    elif request.method == 'DELETE':
        raise NotImplementedError("DELETE currently not supported")




@api_view(['POST'])
def subcategory_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    serializer = SubCategorySerializer(data=request.data)
    if serializer.is_valid():
        subcategory = serializer.save(category=category)
        return Response(SubCategorySerializer(subcategory).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def processorder_view(request):
    orderuser = User.objects.get(id=request.user.id) 
    data = request.data    
    order = Order.objects.create(user=orderuser, ref_code=create_ref_code())
        
    if isinstance(data, list):
        serializer = MyProcessOrderSerializer(data=request.data, many=True)
        
    else:
        serializer = MyProcessOrderSerializer(data=request.data)
        
    if serializer.is_valid():
        processorder = serializer.save(order=order, user=request.user)
        return Response(status=status.HTTP_201_CREATED)
        #return HttpResponse("Question created", status=201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'GET':
        serializer = OrderDetailsSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        raise NotImplementedError("PATCH currently not supported")
    elif request.method == 'DELETE':
        raise NotImplementedError("DELETE currently not supported")



@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def proceed_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'GET':
        serializer = OrderDetailsSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ProceedOrderSerializer(order, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderDetailsSerializer(order).data)
        return Response("Order Updated", status=status.HTTP_204_NO_CONTENT)
        #return Response(serializer.errors)
    elif request.method == 'DELETE':
        order.delete()
        return Response("Order deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def billing_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'GET':
        serializer = BillingDetailSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ProceedOrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderDetailsSerializer(order).data)
        return Response("Order Updated", status=status.HTTP_201_CREATED) 
        #return Response(serializer.errors)
    elif request.method == 'DELETE':
        order.delete()
        return Response("Order deleted", status=status.HTTP_201_CREATED)



'''
class QuestionDetailView(APIView):

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['order_id'])
        serializer = OrderDetailsSerializer(order)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['order_id'])
        serializer = QuestionDetailPageSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionDetailPageSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['order_id'])
        order.delete()
        return Response("Order Deleted", status=status.HTTP_204_NO_CONTENT) 


class ListCreateSongsView(generics.ListCreateAPIView):
    """
    GET songs/
    POST songs/
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_song = Songs.objects.create(
            title=request.data["title"],
            artist=request.data["artist"]





            
        )
        return Response(
            data=SongsSerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )


class SongsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET songs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(SongsSerializer(a_song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            serializer = SongsSerializer()
            updated_song = serializer.update(a_song, request.data)
            return Response(SongsSerializer(updated_song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            a_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
  
class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserUpdateSerialier
    lookup_field = 'username'

    def get_object(self):
        username = self.kwargs["username"]
        return get_object_or_404(User, username=username)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = DeploymentOnUserModel.objects.get(pk=kwargs['pk'])
        serializer = DeploymentOnUserSerializer(object)
        return Response(serializer.data)

class QuestionDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = QuestionDetailPageSerializer
    lookup_url_kwarg = 'question_id'

    def get_queryset(self):
        last_two_days = now() - timedelta(days=2)
        return Question.objects.filter(pub_date__gt=last_two_days)


     def get_queryset(self):
      pk = self.request.GET.get("pk")
      return deployment = DeploymentOnUserModel.objects.get(pk=pk) 
    
'''







    
