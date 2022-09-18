from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', HomeApiView.as_view() ),
    path("posts/", PostView.as_view()),
    path("posts/search/<str:params>/", PostView.as_view()),
    path("posts/<slug:slug>/", PostView.as_view()),  
    path("comment/", CommentView.as_view()),  
    path("comment/<slug:slug>/", CommentView.as_view()),  
    
    
    
    path("authors/", AuthorsView.as_view()),
    path("authors/<slug:url>/posts/", AllSingleAuthorPost.as_view()),
    path("authors/<slug:url>/", AuthorsView.as_view()),
    path("posts/<slug:slug>/related/", PostDetailRelatedView.as_view()),
    
    
    
    
    path("create/", PostCreateView.as_view()),
    path("update/<slug:slug>/", PostCreateView.as_view()),
    path("delete/<slug:slug>/", PostCreateView.as_view()),
    
    
    path("register/", UserCreateView.as_view()),
    path("login/", LoginView.as_view()),
    path("user/profile-create/", ProfileCreateView.as_view()),
    path("author/admin/", AuthorAdminView.as_view()),
    path("author/profile/", AuthorAdminProfileView.as_view()),
    
]
