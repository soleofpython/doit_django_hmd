from django.urls import path
from . import views

urlpatterns = [
    # 댓글 수정페이지 경로를 추가, CBV 스타일로 생성
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    # update_post/<int:pk>/로 접근시 PostUpdate 클래스 사용
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page, name='category_filter'),
    # URL에 있는 pk로 포스트를 찾고, 댓글을 달기 위해 '<int:pk>/new_comment/', views.new_comment 로 설정
    path('<int:pk>/new_comment/', views.new_comment),  
    path('<int:pk>/', views.PostDetail.as_view(), name='post_etail'),
    path('', views.PostList.as_view(), name="post_list"),
    # /blog/category/{self.slug}
    # /blog/category/파이썬
    
]
