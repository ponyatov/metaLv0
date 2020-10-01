#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:mid>
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = CustomUser
		fields = '__all__'
class CustomUserChangeForm(UserChangeForm):
	class Meta(UserCreationForm):
		model = CustomUser
		fields = '__all__'

# / <section:mid>
