from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipeForm
import random
from django.contrib.auth import logout
from .forms import SignUpForm


def home(request):
    recipes = Recipe.objects.all()
    random_recipes = random.sample(list(recipes), min(len(recipes), 5))
    context = {'recipes': random_recipes}
    return render(request, 'home.html', context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'recipe.html', context)

@login_required
def add_edit_recipe(request, recipe_id=None):
    if recipe_id:  # Если передан идентификатор рецепта, значит это редактирование
        recipe = Recipe.objects.get(id=recipe_id)
    else:  # Иначе, это добавление нового рецепта
        recipe = None

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  # Устанавливаем автора рецепта
            recipe.save()
            print(recipe.id)
            return redirect('add_edit_recipe', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'add_edit_recipe.html', {'form': form, 'recipe': recipe})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            print(recipe.id)
            return redirect('add_edit_recipe', recipe_id=recipe.id)
    else:
        form = RecipeForm()

    return render(request, 'add_edit_recipe.html', {'form': form, 'recipe': None})


@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            print(recipe.id)
            return redirect('add_edit_recipe', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'add_edit_recipe.html', {'form': form, 'recipe': recipe})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправляем пользователя на главную страницу
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})



def logout_view(request):
    logout(request)
    # Перенаправляем пользователя на главную страницу или на страницу входа
    return redirect('home')
