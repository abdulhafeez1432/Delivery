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

class CategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('name',) 

class OrderSubCategorySerializer(serializers.ModelSerializer):
    
          
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'quantity', 'price')


    



class ProcessOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessOrder
        fields = ('order', 'quantity', 'subcategory')


class ProcessDetailPageSerializer(OrderSubCategorySerializer):
    order_set = ProcessOrderSerializer(many=True)

    def create(self, validated_data):
        order_validated_data = validated_data.pop('order_set')
        processorder = ProcessOrder.objects.create(**validated_data)
        order_set_serializer = self.fields['order_set']
        for each in order_validated_data:
            each['processorder'] = processorder
        order = order_set_serializer.create(order_validated_data)
        return processorder


class OrderlistSerializer(serializers.ModelSerializer):
    pass



# class ChoiceSerializer(serializers.ModelSerializer):
#     question_text = serializers.CharField(read_only=True, source='question.question_text')

#     class Meta:
#         model = Choice
#         fields = ('id', 'choice_text', 'question', 'question_text')
#         extra_kwargs = {
#             'question': {'write_only': True}
#         }


        



# class VoteSerializer(serializers.ModelSerializer):
# class Meta:
# model = Vote
# fields = '__all__'
# class ChoiceSerializer(serializers.ModelSerializer):
#subcategory = serializers.PrimaryKeyRelatedField(many=True, queryset=SubCategory.objects.filter(category=category_id))
#subcategory = serializers.CharField(source='subcategory.name')

# votes = VoteSerializer(many=True, required=False)
# class Meta:
# model = Choice
# fields = '__all__'
# class PollSerializer(serializers.ModelSerializer):
# choices = ChoiceSerializer(many=True, read_only=True, required=False)
# class Meta:
# model = Poll
# fields = '__all__'



# class SongsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Songs
#         fields = ("title", "artist")

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.artist = validated_data.get("artist", instance.artist)
#         instance.save()
#         return instance
