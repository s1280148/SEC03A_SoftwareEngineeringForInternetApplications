from django import forms
from django.forms import ModelForm, Form, TextInput, Select

from BlogApp.models import User, Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PostCreateForm(ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PostUpdateForm(ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PostSearchForm(Form):
    title = forms.CharField(required=False,
                            widget=TextInput(
                                attrs={
                                    'class': 'form-control'
                                }
                            ))
    content = forms.CharField(required=False,
                              widget=TextInput(
                                  attrs={
                                      'class': 'form-control'
                                  }
                              ))
    author_id = forms.ModelChoiceField(queryset=User.objects.all().filter(is_superuser=False),
                                       empty_label='',
                                       required=False,
                                       widget=Select(
                                           attrs={
                                               'class': 'form-select'
                                           }
                                       ))

    creation_date = forms.DateField(required=False,
                                    widget=TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'autocomplete': 'off'
                                        }
                                    ))
