from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse

def index(request):
    #queries Category model and returns the top five categories
    #categories sorted in descending order by likes
    category_list = Category.objects.order_by('-likes')[:5]

    #queries Page model and returns the top five most viewed pages
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        #returns the category corresponding to the passed in slug
        category = Category.objects.get(slug=category_name_slug)
        
        #return the pages corresponding to the category
        pages = Page.objects.filter(category=category)

        #builds the context dictionary
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    #uses the category.html template to render the view
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    #if the user has submitted (posted) a form to be processed
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            #received the form, so return the user back to the index page
            return redirect('/rango/')
        else:
            #if the form submitted is invalid, print the errors for the user
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    #redirect the user to the index page if the category doesn't exist
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
        
    
    
