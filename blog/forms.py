from django import forms
from .models import Post
from .models import Comment

from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','hook_text', 'content', 'head_image','file_upload','category', 'tags']
        widgets = {
            'content': SummernoteWidget(),
        }
        
# 실제로 현실적으로 작동하는 폼을 생성 
class CommentForm(forms.ModelForm):
    class Meta:
        # Comment 모델에는 여러 필드가 있지만, 여기서는 content 필드만 필요
        model = Comment
        field = ('content',)  
        exclude = ('post', 'author', 'create_at', 'modified_at', )      