from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForms(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = RegisterForms()
    return render(request, 'register.html',{'form':form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            user = RegisterModel.objects.filter(userid=userid, password=password).first()
            if user:
                return redirect('mydetails', userid=user.userid)
            else:
                return redirect('register')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def mydetails(request, userid):
    user = get_object_or_404(RegisterModel, userid=userid)
    return render(request, 'mydetails.html', {'user': user})

def update_details(request, userid):
    user = get_object_or_404(RegisterModel, userid=userid)
    if request.method == "POST":
        form = RegisterForms(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('mydetails', userid=user.userid)
    else:
        form = RegisterForms(instance=user)
    return render(request, 'update_details.html', {'form': form})

def recipe_detail(request, recipe_id, userid):
    user = RegisterModel.objects.get(userid=userid)
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'user':user})

def search_recipe(request, userid):
    user=RegisterModel.objects.get(userid=userid)
    query = request.GET.get('query')
    if query:
        recipes = Recipe.objects.filter(name__icontains=query) | Recipe.objects.filter(ingredients__icontains=query)
    else:
        recipes = Recipe.objects.all()
    return render(request, 'search_recipe.html', {'recipes': recipes, 'user':user})

@login_required
def recipe_list(request,userid):
    user = RegisterModel.objects.get(userid=userid)
    recipes = Recipe.objects.filter(author=user)
    return render(request, 'recipe_list.html', {'recipes': recipes, 'user': user})

@login_required
def add_recipe(request,userid):
    user = RegisterModel.objects.get(userid=userid)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            return redirect('recipe_list', userid=user.userid)
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form, 'user':user})


def edit_recipe(request, id, userid):
    user = RegisterModel.objects.get(userid=userid)
    recipe = get_object_or_404(Recipe, pk=id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            return redirect('recipe_list', userid=user.userid)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'edit_recipe.html', {'form': form, 'recipe': recipe, 'user':user})

def delete_recipe(request, recipe_id,userid):
    user = RegisterModel.objects.get(userid=userid)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    return redirect('recipe_list', userid=user.userid)