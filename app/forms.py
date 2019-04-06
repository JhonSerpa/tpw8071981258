from django import forms
from app.models import MediaAuthor


class AddReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, label="Comment")
    rate = forms.IntegerField(max_value=5, min_value=0, label="Rate ")


class MediaInsertForm(forms.Form):
    Name = forms.CharField(label="Name", max_length=100)
    Description = forms.CharField(label="Description", max_length=200)
    Author = forms.ModelChoiceField(label="Author", queryset=MediaAuthor.objects.all())

    Img = forms.ImageField(label="Profile picture")


class AuthorInsertForm(forms.Form):
    Name = forms.CharField(label="First name", max_length=100)
    Surname = forms.CharField(label="Surname", max_length=100)
    Img = forms.ImageField(label="Profile picture")


class SearchData(forms.Form):
    #CHOICES = (
    #    (1, 'Media'),
    #    (2, 'Author'),
    #)

    #Type = forms.ChoiceField(choices=CHOICES)
    Search = forms.CharField(max_length=100)

