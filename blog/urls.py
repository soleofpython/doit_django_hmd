from django.urls import path
from . import views

urlpatterns = [
    # update_post/<int:pk>/로 접근시 PostUpdate 클래스 사용
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page, name='category_filter'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_etail'),
    path('', views.PostList.as_view(), name="post_list"),
    # /blog/category/{self.slug}
    # /blog/category/파이썬
    
]
