from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic.base import View

from Challenge import backends
from Challenge.forms import LoginForm, SignUpForm
from Challenge.models import Shop, Profile


class HomeView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Please login")
            return redirect('challenge:login')
        shops = Shop.objects.exclude(id__in=request.user.profile.banned_shops.all().values('id')).order_by('distance')
        # ---------------- Search ----------------
        search = request.GET.get('search', None)
        if search is not None:
            shops = shops.filter(name__icontains=search)
        # ---------------- Pagination ----------------
        page = request.GET.get('page', 1)
        paginator = Paginator(shops, 8)
        try:
            shops = paginator.page(page)
        except PageNotAnInteger:
            shops = paginator.page(1)
        except EmptyPage:
            shops = paginator.page(paginator.num_pages)

        context = {
            'shops': shops
        }
        return render(request, 'challenge/index.html', context)

    def post(self, request):
        return redirect('challenge:home')


class LoginView(View):

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('challenge:home')
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'challenge/login.html', context)

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('challenge:home')
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['email'], password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('challenge:home')
            else:
                print(str(user))
        else:
            messages.error(request, "Invalid email or password!")
        context = {
            'login_form': login_form
        }
        return render(request, 'challenge/login.html', context)

class RegisterView(View):

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('challenge:home')
        singup_form = SignUpForm()
        context = {
            'signup_form': singup_form
        }
        return render(request, 'challenge/signup.html', context)

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('challenge:home')
        singup_form = SignUpForm(request.POST or None)
        if singup_form.is_valid():
            user = User.objects.create(email=singup_form.cleaned_data['email'])
            user.set_password(singup_form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('challenge:home')
        else:
            messages.error(request, "Invalid data, please correct errors and try again!")
        context = {
            'signup_form': singup_form
        }
        return render(request, 'challenge/signup.html', context)


class PreferredShopsView(View):

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect('challenge:login')
        preferred_shops = user.profile.preferred_shops.all()
        # ---------------- Pagination ----------------
        page = request.GET.get('page', 1)
        paginator = Paginator(preferred_shops, 8)
        try:
            preferred_shops = paginator.page(page)
        except PageNotAnInteger:
            preferred_shops = paginator.page(1)
        except EmptyPage:
            preferred_shops = paginator.page(paginator.num_pages)

        context = {
            'preferred_shops': preferred_shops
        }
        return render(request, 'challenge/preferred_shops.html', context)

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('challenge:login')
        return redirect('challenge:preferred_shops')

class LogOut(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('challenge:login')


    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('challenge:login')

@login_required
def like_shop(request):
    shop_id = request.POST.get('shop', None)
    status = False
    message = ""
    if shop_id is not None:
        shop = Shop.objects.filter(id=shop_id)
        if shop.exists():
            shop = shop.first()
            profile = request.user.profile
            if shop not in profile.preferred_shops.all():
                profile.preferred_shops.add(shop)
                status = True
                message = "Shop added to your preferred list successflly"
            else:
                message = "Shop already exists in your preferred list"
        else:
            message = "No shop found, please reload the page and try again!"
    else:
        message = "An error occurred, please try again!"

    context = {
        'status': status,
        'message': message
    }

    return JsonResponse(context, safe=False)

@login_required
def dislike_shop(request):
    shop_id = request.POST.get('shop', None)
    status = False
    profile = request.user.profile
    message = ""
    if shop_id is not None:
        shop = Shop.objects.filter(id=shop_id)
        if shop.exists():
            shop = shop.first()
            if shop not in profile.banned_shops.all():
                profile.banned_shops.add(shop)
                profile.preferred_shops.remove(shop)
                status = True
                message = "Shop disliked successflly"
            else:
                message = "Shop already exists in your banned list"
        else:
            message = "No shop found, please reload the page and try again!"
    else:
        message = "An error occurred, please try again!"

    no_more_shops = profile.banned_shops.all().count() == Shop.objects.all().count()

    context = {
        'status': status,
        'message': message,
        'no_more_shops': no_more_shops
    }

    return JsonResponse(context, safe=False)

@login_required
def remove_shop(request):
    shop_id = request.POST.get('shop', None)
    status = False
    profile = request.user.profile
    message = ""
    if shop_id is not None:
        shop = Shop.objects.filter(id=shop_id)
        if shop.exists():
            shop = shop.first()
            if shop not in profile.banned_shops.all():
                profile.preferred_shops.remove(shop)
                status = True
                message = "Shop removed from your list successflly"
            else:
                message = "Shop already exists in your banned list"
        else:
            message = "No shop found, please reload the page and try again!"
    else:
        message = "An error occurred, please try again!"

    no_more_shops = profile.preferred_shops.all().count() == 0

    context = {
        'status': status,
        'message': message,
        'no_more_shops': no_more_shops
    }

    return JsonResponse(context, safe=False)
















