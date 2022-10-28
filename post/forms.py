from django import forms
from pscmodels.models import Posts, Comments
from taggit.forms import TagWidget
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content', 'category','image_file','tags']

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', 'required': 'True','placeholder' : 'Title'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'required': 'True','placeholder' : 'Description'}),
            'category': forms.Select(attrs={'class':'form-control', 'required': 'True'}),
            'image_file': forms.FileInput(attrs={'class':'form-control'}),
            'tags': TagWidget(attrs={'class':'form-control', 'required': 'True', 'placeholder':'Comma seperated values' })
            # 'tags': forms.TextInput(attrs={'class':'form-control', 'required': 'True', 'placeholder':'Comma seperated values' }),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['comment']
  