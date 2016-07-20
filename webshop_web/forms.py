from django import forms


class ClientForm(forms.Form):
    required_css_class = 'required-field'

    name = forms.CharField(label='', strip=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Name',
                                                         'size': '30',
                                                         'class': ''})
                           )
    city = forms.CharField(label='', strip=True,
                           widget=forms.TextInput(attrs={'placeholder': 'City',
                                                         'size': '30',
                                                         'class': ''})
                           )
    address = forms.CharField(label='', strip=True,
                              widget=forms.TextInput(attrs={'placeholder': 'address',
                                                            'size': '30',
                                                            'class': ''})
                              )
    mobile = forms.CharField(label='', strip=True,
                             widget=forms.TextInput(attrs={'placeholder': 'mobile',
                                                           'size': '30',
                                                           'class': ''})
                             )
    comment = forms.CharField(label='', required=False, strip=True,
                              widget=forms.Textarea(attrs={'placeholder': 'You can tell us more information',
                                                           'cols': '29',
                                                           'class': ''}))
