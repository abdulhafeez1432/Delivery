from rest_framework import serializers
from app.models import *

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    #password2 = serializers.CharField(
    #    style={"input_type": "password"}, write_only=True, label="Confirm password")


    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_customer = True
        user.save()
        ProfileCustomer.objects.create(user=user)
        return user


    # def create(self, validated_data):
    #     username = validated_data["username"]
    #     email = validated_data["email"]
    #     password = validated_data["password"]
    #     password2 = validated_data["password2"]
    #     if (email and User.objects.filter(email=email).exclude(username=username).exists()):
    #         raise serializers.ValidationError(
    #             {"email": "Email addresses must be unique."})
    #     if password != password2:
    #         raise serializers.ValidationError(
    #             {"password": "The two passwords differ."})
    #     user = User(username=username, email=email)
    #     user.set_password(password)
    #     user.is_customer = True
    #     user.save()
    #     ProfileCustomer.objects.create(user=user)
    #     return user


 


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ProfileCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProfileCustomer
        fields = ('phone_number', 'gender', 'address')



class SubCategorySerializerSE(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('name',) 


class SubCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)


    def create(self, validated_data):
        return SubCategory.objects.create(**validated_data)

class CategoryListPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'address')
    
    
class CategoryDetailsSerializer(CategoryListPageSerializer):
    subcategory = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('name', 'address', 'subcategory',)



class ProcessOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessOrder
        fields = ('quantity', 'user')

        read_only_fields = ('user', ) 

    
    
class SubCategoryOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ('quantity', 'id')

        

class MyProcessOrderSerializer(serializers.ModelSerializer):

    #subcategory_name = serializers.RelatedField(source='subcategory.id', read_only=True)
    #subcategory_set = SubCategoryOrderSerializer(many=True)
    #subcategory = serializers.StringRelatedField(source='subcategory.id', read_only=True)



    class Meta:
        model = ProcessOrder
        fields = ('quantity', 'subcategory', 'user')

        read_only_fields = ('user', ) 

    def create(self, validated_data):
        return ProcessOrder.objects.create(**validated_data)

    
class OrderListPageSerializer(serializers.ModelSerializer):

    class meta:
        model = Order
        fields = ('ref_code')


class ProcessOrderDetailsSerializer(serializers.ModelSerializer):

    #subcategory_name = serializers.RelatedField(source='subcategory.id', read_only=True)
    #subcategory_set = SubCategoryOrderSerializer(many=True)
    #subcategory = serializers.StringRelatedField(source='subcategory.id', read_only=True)
    get_price_cost = serializers.CharField(read_only=True)
    get_good_name = serializers.CharField(read_only=True)




    class Meta:
        model = ProcessOrder
        fields = ('quantity', 'get_price_cost', 'get_good_name')
 

    def create(self, validated_data):
        return ProcessOrder.objects.create(**validated_data)

class OrderDetailsSerializer(OrderListPageSerializer):

    order = ProcessOrderDetailsSerializer(many=True, read_only=True)
    get_total_cost =  serializers.CharField(read_only=True)


    class Meta:
        model = Order
        fields = ('ref_code', 'order', 'get_total_cost')


class ProceedOrderSerializer(serializers.ModelSerializer):

    #order = MyProcessOrderSerializer(many=True, read_only=True)


    class Meta:
        model = Order
        fields = ('shipping_address', 'package', 'ordernote')


class BillingDetailSerializer(OrderListPageSerializer):

    order = ProcessOrderDetailsSerializer(many=True, read_only=True)
    get_package = serializers.CharField(read_only=True)
    get_grant_total = serializers.CharField(read_only=True)
    get_total_cost =  serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('order', 'get_grant_total', 'get_total_cost', 'ordernote', 'get_package' , 'shipping_address' )



