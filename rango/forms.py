from django import forms
from rango.models import Category, Page

class CategoryForm(forms.ModelForm):
    'category form'
    name = forms.CharField(max_length=128, 
                           help_text='Please enter the category name.')
    views = forms.IntegerField(widget=forms.HiddenInput, initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput, initial=0)
    slug = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta(object):
        'meta'
        model = Category
        fields = ('name', )

class PageForm(forms.ModelForm):
    'page form'
    title = forms.CharField(max_length=128,
                            help_text='Please enter the title of the page')
    url = forms.CharField(max_length=200,
                          help_text='Please enter the url of the page')
    views = forms.IntegerField(widget=forms.HiddenInput, initial=0)

    class Meta(object):
        'meta'
        model = Page
        exclude = ('category', )

    def clean(self):
        'some preproccessing stuff'
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data
