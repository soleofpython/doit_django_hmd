from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page, name='category_filter'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_etail'),
    path('', views.PostList.as_view(), name="post_list"),
    # /blog/category/{self.slug}
    # /blog/category/파이썬
    
]
