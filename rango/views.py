from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

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
    
    
