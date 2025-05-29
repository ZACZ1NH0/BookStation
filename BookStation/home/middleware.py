from django.shortcuts import redirect
from django.urls import reverse

class RoleRedict:
    def __init__(self,get_reponses):
        self.get_reponses=get_reponses

    def __call__(self,request):
        if request.user.is_authenticated and request.path in ['/', '/login/', '/accounts/login/']:
            user = request.user
