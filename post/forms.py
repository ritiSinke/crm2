from django import forms
from .models import Post 


#  model form helps to create a form based on the model fields


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        # use lai kun kun fields haru form ma dekhaucha bhanne kura garna parxa
        fields =['title', 'content', 'category', 'is_draft', 'image']



class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'is_draft', 'image']