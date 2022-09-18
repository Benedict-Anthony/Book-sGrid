from rest_framework import serializers
from blog.models import Post, Caption, Comment
from users.models import User, Profile

class CaptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caption
        fields = ["tag",]
       
    
class PostSerializer(serializers.ModelSerializer):
    caption = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField()
    class Meta:
        model = Post
        fields = "__all__"
        
  
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["name", "comment", "post"] 

      
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', "user"] 

        
class CreatPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name","last_name","write_about", "about", "full_name", "image", "phone", "facebook_url", "instagram_url", "twitter_url", "linkedin_url","user" ]
    
  

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ["id","email", "profile","url"]
        

        

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =["email", "username", "password"]
        
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        else:
            raise ValueError("password can not be None")
        instance.save()
        return instance