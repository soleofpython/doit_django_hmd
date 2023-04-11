from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag
from .forms import CommentForm

# 첫번째 Tag 모델은 인스턴스, 두번째는 bool 형태의 값 의미
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied
from .forms import PostForm
from django.db.models import Q

# PostCreate 클래스를 수정
# UserPassesTestMixin를 Parameter로 추가, 

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    templates_name = 'blog/post_form.html'
    # fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    
    # test_func함수 추가 : 접근가능 사용자를 Staff 이상으로 한정
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            # form_valid 함수 결과값을 response라는 변수에 저장
            response= super(PostCreate, self).form_valid(form)
            # name="tags_str"인 input의 값을 호출함.
            tags_str = self.request.POST.get("tags_str")
            # tags_str로 받은 값의 쉼표를 세미콜론으로 모두 변경, split해서 리스트로 tags_list에 저장
            if tags_str :
                tags_str = tags_str.strip() 
                
                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';')
                
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
                    
            return response
            
             
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



# PostUpdate 클래스를 CBV 스타일 적용        
# CreateView 대신 UpdateView 사용, 기존 작성자가 이미 존재하므로 form_valid 함수를 사용하기 않음.
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']
    
    # CBV로 View를 만들 때, 원하는 html 파일을 템플릿 파일로 설정
    template_name = 'blog/post_update_form.html'
    
    # dispatch() 함수는 방문자가 서버에 GET 방식인지 POST 방식으로 요청했는지 판단
    # request.user가 로그인한 상태
    # Post 인스턴스의 author 필드가 request.user와 동일한 경우에만 dispatch() 함수가 역할 가능
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        

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
        # PostDetail 클래스의 get_context_data() 함수에서 CommentForm을 comment_form으로 전달
        context['comment_form'] = CommentForm
        
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
    
# 함수형 view 정의, tag 필터링   
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

# 함수형 view 정의, category 필터링  
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
    
def new_comment(request, pk):
    # 비정상적인 방법으로 new_comment에 접근하려는 시도에는 PermissionDenied 발생
    if request.user.is_authenticated :
        post = get_object_or_404(Post, pk=pk)
        
        if request.method == 'POST':
            # POST 방식으로 들어온 정보를 CommentForm 형태로 가져옴
            comment_form = CommentForm(request.POST)
            # 폼이 유효하게 작성되었으면 해당 내용을 신규 레코드로 만들어 DB에 저장
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect (comment.get_absolute_url())
        else:
            return redirect (post.get_absolute_url())
    else:
        raise PermissionDenied
            
            
            
            