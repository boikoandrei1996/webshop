from django import forms


class SearchForm(forms.Form):
    search_text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search',
                                                                'class': 'form-control input-sm'}))


class DeleteProductForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    price = forms.FloatField(label='Price per one')
    amount = forms.IntegerField(label='Amount')


class ClientForm(forms.Form):
    name = forms.CharField(label='Your name',
                           widget=forms.TextInput(attrs={'placeholder': 'Name',
                                                         'class': ''})
                           )
    city = forms.CharField(label='Your city',
                           widget=forms.TextInput(attrs={'placeholder': 'City',
                                                         'class': ''})
                           )
    address = forms.CharField(label='Your address',
                              widget=forms.TextInput(attrs={'placeholder': 'address',
                                                            'class': ''})
                              )
    mobile = forms.CharField(label='Your mobile',
                             widget=forms.TextInput(attrs={'placeholder': 'mobile',
                                                           'class': ''})
                             )
    comment = forms.CharField(label='Some comment for us', required=False,
                              widget=forms.Textarea(attrs={'placeholder': 'You can tell us more information',
                                                           'class': ''}))
