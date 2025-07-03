from django import forms
from .models import Post ,Comment



#  model form helps to create a form based on the model fields


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # use lai kun kun fields haru form ma dekhaucha bhanne kura garna parxa
        fields =['title', 'content', 'category', 'is_draft', 'image']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'
           
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'

