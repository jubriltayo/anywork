from django import forms
from .models import Professional

class ProfessionalForm(forms.ModelForm):
    # OPTIONS = [
    #     ('Tutorship', 'Tutorship'),
    #     ('Transportation', 'Transportation'),
    #     ('Food', 'Food'),
    #     ('Cleaning', 'Cleaning')
    # ]
    # name                = forms.CharField(label='', max_length=128, 
    #                                       widget=forms.TextInput(
    #                                           attrs={
    #                                               "placeholder": "Name"
    #                                           }
    #                                       ))
    # email               = forms.EmailField(label='', 
    #                                        widget=forms.EmailInput(
    #                                            attrs={
    #                                                "placeholder": "Email"
    #                                            }
    #                                        ))
    # phone_number        = forms.CharField(label='', max_length=20,
    #                                       widget=forms.TextInput(
    #                                           attrs={
    #                                               "placeholder": "Phone number"
    #                                           }
    #                                         ))
    # address             = forms.CharField(label='',
    #                                       widget=forms.Textarea(
    #                                           attrs={
    #                                               "placeholder": "Address", 
    #                                               "rows": 10,
    #                                               "cols": 60
    #                                           }
    #                                       ))
    # service             = forms.ChoiceField(widget=forms.RadioSelect, choices=OPTIONS)
    # years_of_experience = forms.IntegerField(min_value=0, max_value=50)
    # qualification       = forms.CharField(label='', 
    #                                       widget=forms.Textarea(
    #                                           attrs={
    #                                               "placeholder": "Qualification", 
    #                                               "rows": 10,
    #                                               "cols": 40
    #                                           }
    #                                       ))
    # price               = forms.IntegerField(initial=500, 
    #                                          min_value=0, 
    #                                          max_value=10000000
    #                                          )
    
    class Meta:
        model = Professional
        fields = [
            'name',
            'email',
            'phone_number',
            'address',
            'service',
            'years_of_experience',
            'qualification',
            'price'
        ]

class RawProfessionalForm(forms.Form):
    OPTIONS = [
        ('Tutorship', 'Tutorship'),
        ('Transportation', 'Transportation'),
        ('Food', 'Food'),
        ('Cleaning', 'Cleaning')
    ]
    name                = forms.CharField(label='', max_length=128, 
                                          widget=forms.TextInput(
                                              attrs={
                                                  "placeholder": "Name"
                                              }
                                          ))
    email               = forms.EmailField(label='', 
                                           widget=forms.EmailInput(
                                               attrs={
                                                   "placeholder": "Email"
                                               }
                                           ))
    phone_number        = forms.CharField(label='', max_length=20,
                                          widget=forms.TextInput(
                                              attrs={
                                                  "placeholder": "Phone number"
                                              }
                                            ))
    address             = forms.CharField(label='',
                                          widget=forms.Textarea(
                                              attrs={
                                                  "placeholder": "Address", 
                                                  "rows": 5,
                                                  "cols": 25
                                              }
                                          ))
    service             = forms.ChoiceField(widget=forms.RadioSelect, choices=OPTIONS)
    years_of_experience = forms.IntegerField(min_value=0, max_value=50)
    qualification       = forms.CharField(label='', 
                                          widget=forms.Textarea(
                                              attrs={
                                                  "placeholder": "e.g. BSc", 
                                                  "rows": 5,
                                                  "cols": 25
                                              }
                                          ))
    price               = forms.IntegerField(initial=500, 
                                             min_value=0, 
                                             max_value=10000000
                                             )   