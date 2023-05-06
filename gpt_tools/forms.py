from django import forms

class SummaryForm(forms.Form):
    """
    Youtubeの動画のURLを入力するフォーム
    """
    url = forms.CharField(label='URL', max_length=100)