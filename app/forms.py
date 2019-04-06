from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as uu


class AddReviewForm(forms.Form):
    review = forms.CharField(max_length=1000, label="Comment ")
    rate = forms.IntegerField(max_value=5, min_value=0, label="Rate ")


from app.models import MediaAuthor, User, Media


class MediaInsertForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['name', 'description', 'author', 'img']


class AuthorInsertForm(forms.ModelForm):
    class Meta:
        model = MediaAuthor
        fields = ['name','surname','img']



class SearchData(forms.Form):
    CHOICES = (
        (1, 'Media'),
        (2, 'Author'),
    )

    Type = forms.ChoiceField(choices=CHOICES)
    Search = forms.CharField(max_length=100)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = uu
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['img']

