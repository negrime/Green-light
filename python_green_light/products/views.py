from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, User, Category
from django.utils import timezone


# Create your views here.
def home(request):
    products = Product.objects.order_by('-votes_total')
    return render(request, 'products/home.html', {'products': products, 'user': request.user})


def profile(request):
    products = Product.objects.filter(hunter=request.user)
    return render(request, 'products/profile.html', {'products': products, 'user': request.user, 'liked_projects': request.user.profile.liked_projects.all()})


def delete(request, id):
    try:
        person = Product.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/")
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


@login_required
def edit(request, id):
    try:
        product = Product.objects.get(id=id)

        if request.method == "POST":
            if request.POST['title'] and request.POST['body'] and request.POST['url']:
                product.title = request.POST.get("title")  # ['title']
                product.body = request.POST.get("body")  # 'body']
                if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                    product.url = request.POST['url']
                else:
                    product.url = 'http://' + request.POST['url']
                if len(request.FILES) != 0:
                    product.icon = request.FILES['icon']
                    product.image = request.FILES['image']
                product.pub_date = timezone.datetime.now()
                product.category = Category.objects.get(name=request.POST['category'])
                product.save()
                return redirect('/products/' + str(product.id))
            else:
                return redirect('/products/edit/' + str(product.id))
                #return render(request, 'products/edit/' + str(product.id) + '.html', {'error': '** All fields are required **'})
        else:
            categories = Category.objects.all()
            return render(request, 'products/edit.html', {'product': product, 'categories': categories})
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and len(request.FILES) != 0:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.category = Category.objects.get(name=request.POST['category'])
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': '** All fields are required **'})
    else:
        categories = Category.objects.all()
        return render(request, 'products/create.html', {'categories': categories})

@login_required
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        isVoted = request.user.profile.liked_projects.get(id=product_id) != None
    except Product.DoesNotExist:
        isVoted = False
    finally:
        return render(request, 'products/detail.html', {'product': product, 'user': request.user, 'isVoted': isVoted})


@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        request.user.profile.balance -= 1
        product.votes_total += 1
        request.user.profile.liked_projects.add(product_id)
        product.save()
        request.user.profile.save()
        return redirect('/products/' + str(product.id))



@login_required(login_url='/accounts/signup')
def downvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        request.user.profile.balance += 1
        product.votes_total -= 1
        request.user.profile.liked_projects.remove(product_id)
        product.save()
        request.user.profile.save()
        return redirect('/products/' + str(product.id))



