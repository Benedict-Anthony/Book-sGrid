from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer, UserSerializer, CreatPostSerializer, UserCreateSerializer, ProfileSerializer, CommentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from blog.models import Post, Comment
from users.models import User, Profile
from django.http import Http404
from django.utils.text import slugify
from django.db.models import Q

class HomeApiView(APIView):
    def get(self, request):
        api = {
            "api/posts":"all posts",
            "api/posts/search/params":"filtering",
            "api/posts/slug":"single post",
            "api/posts/slug/related":"post related to the single post",
            "api/authors":"all authors",
            "api/authors/url":"Single author",
            "api/authors/url/posts":"Single author's posts",
        }
        return Response(api)

class PostView(APIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
   
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all().order_by("-created_at")
        searchParams = kwargs.get("params", None)
        slug = kwargs.get("slug", None)
        if searchParams is not None:
            queryset = Post.objects.filter(Q(title__icontains=searchParams) | Q(title__istartswith=searchParams) | Q(title__iendswith=searchParams)).order_by("-created_at")
        
            serializer = self.serializer_class(queryset, many=True)
            return Response({"data":serializer.data})
        if slug is not None:
            try:
                queryset = Post.objects.get(slug=slug)
            except:
                raise Http404
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response({"data":serializer.data})

    
class PostDetailRelatedView(APIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, slug):
        try:
            post = Post.objects.get(slug=slug)
        except:
            raise Http404
        
        caption = post.caption.all()
        
        related_post = Post.objects.filter(caption__in=caption).exclude(slug=slug)
        
        serializer = self.serializer_class(related_post, many=True)
        
        return Response(serializer.data)

class CommentView(APIView):
    serialier_class = CommentSerializer
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug", None)
        quaryset = Comment.objects.all()
        serializer = self.serialier_class(quaryset, many=True).data
        if slug is not None:
            try:
                post = Post.objects.get(slug=slug)
            except:
                raise Http404
            
            quaryset = post.comment.all()
            serializer = self.serialier_class(quaryset, many=True).data
            
            return Response(serializer)
        return Response()
            
    def post(self, request, *args, **kwargs):
        serializer = self.serialier_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
class AuthorsView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        url = kwargs.get("url", None)
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True).data
        
        if url is not None:
            try:
                queryset = User.objects.get(url=url)
            except:
                raise Http404
            serializer = self.serializer_class(queryset)
            return Response(serializer.data) 
        return Response({"data":serializer})
    
      
class AllSingleAuthorPost(APIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, url):
        author = User.objects.get(url=url)
        posts = author.author.all().order_by("-created_at")
        
        serializer = self.serializer_class(posts, many=True).data
        return Response({"data":serializer})

 
class PostCreateView(APIView):
    serializer_class = CreatPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request, slug):
        try:
            queryset = Post.objects.get(slug=slug)
        except:
            raise Http404
        serializer = self.serializer_class(queryset)
        
        return Response(serializer.data)
    
    def post(self, request,  *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, slug):
        try:
            post = Post.objects.get(slug=slug)
            print(post)
        except:
            print("error")
        serializer = self.serializer_class(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
 
class LoginViewSerializer(TokenObtainPairSerializer):
     @classmethod
     def get_token(cls, user):
         token = super().get_token(user)
         token["id"] = user.id
         token["email"]= user.email
         
         return token
     
class LoginView(TokenObtainPairView):
    serializer_class = LoginViewSerializer     
        
    
class UserCreateView(APIView):
    serializer_class = UserCreateSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request):
        return Response({"message":"put request sent"})
    
       
class ProfileCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProfileSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except:
            pass
        
        seriliazer = self.serializer_class(profile).data
        return Response(seriliazer)
        
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        first_name =serializer.validated_data["first_name"]
        last_name =serializer.validated_data["last_name"]
        user =serializer.validated_data["user"]
        url = slugify(f'{first_name} {last_name}')
        
        user.url = url
        user.save()
        serializer.save()
      
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def put(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except:
            return Response({"data":None})
        
        serializer = self.serializer_class(data=request.data, instance=profile)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AuthorAdminView(APIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        posts = user.author.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)
    
class AuthorAdminProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except:
            return Response({"data":None}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(profile)
       
        return Response(serializer.data)
 
 
   