from django import forms

from clientapp.models import City

from .models import Cat, sub, Product


class cityform(forms.ModelForm):
    class Meta:
        model = City
        fields='__all__'

class catform(forms.ModelForm):
    class Meta:
        model = Cat
        fields='__all__'

class subcatform(forms.ModelForm):
    class Meta:
        model = sub
        fields = '__all__'

class proform(forms.ModelForm):
    class Meta:
        model=Product
        fields= ['proname','pimg','prod','price','Category_id','sub_id']