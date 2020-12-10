from django.urls import path
from users.views import Login, Profile, Registration, ProfileEdit, Logout, AdminPanel

app_name = 'users'
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', Registration.as_view(), name='registration'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile_update/', ProfileEdit.as_view(), name='profile_edit'),
    path('admin_panel/', AdminPanel.as_view(), name='admin_panel'),
]
