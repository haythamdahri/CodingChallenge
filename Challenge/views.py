from django.shortcuts import render, redirect


# Create your views here.
from django.views.generic.base import View


class HomeView(View):
    def get(self, request):
        pass

    def post(self, request):
        return redirect('challenge:home')