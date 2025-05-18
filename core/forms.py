from django.contrib.auth.models import User
from django import forms
from .models import UserAddress,Profile
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class Registration(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=10, required=True)
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile', 'gender', 'profile_image', 'password1', 'password2']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name[0].isdigit():  # Check if first character is a digit
            raise ValidationError("First name cannot start with a number.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name[0].isdigit():  # Check if first character is a digit
            raise ValidationError("Last name cannot start with a number.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():  # Check if email already exists
            raise ValidationError("This email is already registered.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile.isdigit():  # Check if mobile contains only digits
            raise ValidationError("Mobile number should contain only numbers.")
        if len(mobile) != 10:  # Check if mobile is exactly 10 digits
            raise ValidationError("Mobile number must be 10 digits.")
        return mobile

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Ensure email is saved to User model
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                mobile=self.cleaned_data['mobile'],
                gender=self.cleaned_data['gender'],
                profile_image=self.cleaned_data.get('profile_image'),
            )
        return user

class UserDataChange(UserChangeForm):
    password = None  # hide password field

    mobile = forms.CharField(max_length=15, required=True)
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.profile_instance = kwargs.pop('profile_instance', None)
        super().__init__(*args, **kwargs)

        if self.profile_instance:
            self.fields['mobile'].initial = self.profile_instance.mobile
            self.fields['gender'].initial = self.profile_instance.gender
            self.fields['profile_image'].initial = self.profile_instance.profile_image

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name[0].isdigit():
            raise ValidationError("First name cannot start with a number.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name[0].isdigit():
            raise ValidationError("Last name cannot start with a number.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        # Check if email is being changed
        if hasattr(self.instance, 'email') and self.instance.email != email:
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("This email is already registered.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile.isdigit():
            raise ValidationError("Mobile number should contain only numbers.")
        if len(mobile) != 10:
            raise ValidationError("Mobile number must be 10 digits.")
        return mobile

    def save(self, commit=True):
        user = super().save(commit=False)
        # Update email in User model if changed
        if 'email' in self.cleaned_data:
            user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile = self.profile_instance
            
            if profile:
                profile.first_name = self.cleaned_data.get('first_name', profile.first_name)
                profile.last_name = self.cleaned_data.get('last_name', profile.last_name)
                profile.email = self.cleaned_data.get('email', profile.email)
                profile.mobile = self.cleaned_data['mobile']
                profile.gender = self.cleaned_data['gender']
                
                # Handle profile image update
                new_image = self.cleaned_data.get('profile_image')
                if new_image:
                    # Delete old image if it exists
                    if profile.profile_image:
                        profile.profile_image.delete(save=False)
                    profile.profile_image = new_image
                
                profile.save()
        return user

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['fullName','state','city','area','block','landmark','pin','mobile','addressType']

    