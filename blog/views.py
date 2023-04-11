from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Tag
from .forms import PostForm
from django.db.models import Q

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    templates_name = 'blog/post_form.html'
    # fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
    
#     return render(
#         request,
#         'blog/index.html',
#         {'posts' : posts,}
    # )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'tag' : tag,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
        }
    )
    

class PostList(ListView):
    model = Post
    # post_list.html : class 이름_list.html
    # 내부적으로 정의가 되어있기 때문에 생략 가능
    # 파일명을 위에 있는 규칙으로 하지 않을 경우 명시해 줘야 함
    # template_name = 'blog/post_list.html'
    # template_name = 'blog/index.html'
    
    ordering = '-pk'
    # 한 페이지당 보여줄 post 갯수 정하기
    paginate_by = 2
    
    def get_context_data(self, **kwargs): 
        
        context = super(PostList,self).get_context_data()
        context['categories'] = Category.objects.all()
        # Post 테이블에서 category 필드를 선택안한 포스트의 갯수
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        
        return context
    
    
class PostDetail(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs): 
        
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        # Post 테이블에서 category 필드를 선택안한 포스트의 갯수
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        
        return context
    
    #template_name = 'blog/post_detail.html'  
    
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
    
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post' : post,
#         }
#     )

def category_page(request, slug):
    # 선택한 슬러그의 해당하는 카테고리 테이블의 레코드
    category = Category.objects.get(slug=slug)
    context = {
        # Post 테이블에서 선택한 카테고리의 레코드만 필터링
        'post_list' : Post.objects.filter(category=category),
        # 카테고리 테이블의 목록을 모두 가져옴
        'categories' : Category.objects.all(),
        # Post 테이블에서 카테고리 필드를 선택안 한 포스트의 갯수
        'no_category_post_count' : Post.objects.filter(category=None).count(),
        # 선택한 카테고리의 레코드
        'category' : category
    }    
    # print(context)
    return render(
        request,
        'blog/post_list.html',
        context
    )
    
class PostSearch(PostList):
    paginate_by = None
    
    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
         | Q(content__contains=q)).distinct()
        
        return post_list
    
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        # context[""] =['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        
        return context
    
    # | Q(content__contains=q)