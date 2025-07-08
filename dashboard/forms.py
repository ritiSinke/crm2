from django import forms
from post.models import Category 

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # use lai kun kun fields haru form ma dekhaucha bhanne kura garna parxa
        fields =['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'
