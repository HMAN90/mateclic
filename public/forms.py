from django import forms
from public.models import User
from public.models import CustomUser
from public.models import Equipment
from public.models import Rent
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('confirmationCode','confirmed','companyName')
class RegisterProviderForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('confirmationCode','confirmed','companyName','role')
class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        exclude = ('owner',)
class RentFirstForm(forms.ModelForm):
    class Meta:
        model = Rent
        exclude = ('equipment','paymentMethod','rentStart','rentEnd','receiptCode','customer','state','mobileMoneyPhone','rentTotalAmount','currency','paymentToken','paymentId')
class SettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        #exclude = ('confirmationCode','confirmed','email','countryCode','phone','role','password')
        fields = ('first_name','last_name','companyName','summary','logo')
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        # Link the form to the default User model
        model = CustomUser 
        # Explicitly list all fields, including the built-in and custom ones
        #fields = UserCreationForm.Meta.fields + ('email',)
        #exclude = ('username',)
        fields = ('email','first_name','last_name','countryCode','phone','role')
        
class CustomProviderCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        label="Votre prénom",
        widget=forms.TextInput(attrs={'placeholder': 'Insérez votre prénom'})
    )
    last_name = forms.CharField(
        label="Votre nom",
        widget=forms.TextInput(attrs={'placeholder': 'Insérez votre nom'})
    )

    countryCode = forms.IntegerField(
        label="Code pays",
        widget=forms.NumberInput(attrs={'value': 243})
        
    )
    phone = forms.CharField(
        label="Téléphone",
        widget=forms.TextInput(attrs={'placeholder': 'Votre numéro de téléphone'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Votre mot de passe'}),
        label="Mot de passe"
    )
    # Recommended: Add a field for confirmation to catch typos
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez votre mot de passe'}),
        label="Confirmez votre mot de passe"
    )
    
    class Meta:
        # Link the form to the default User model
        model = CustomUser 
        # Explicitly list all fields, including the built-in and custom ones
        #fields = UserCreationForm.Meta.fields + ('email',)
        #exclude = ('username',)
        fields = ('email','first_name','last_name','countryCode','phone')