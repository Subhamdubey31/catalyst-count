
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_page , name='login_page'),
    path('register/', register_page , name='register_page'),  
    path('uploaded_data/', uploaded_data_view, name='uploaded_data'),
    path('query_builder/', query_builder, name='query_builder'),
    path('user/', user, name='user'),
    path('add_user/', add_user, name='add_user'),

]
