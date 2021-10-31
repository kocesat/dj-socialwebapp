from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from account.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required
def image_list(request):
    images = Image.objects.all()
    return render(request, 'images/image/list.html', {
        'images': images,
        'section': 'images'
    })


@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)    
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to the image
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            # redirect to new created image detail page
            return redirect(new_item.get_absolute_url())
    else:
        # build the form with data provided by bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    
    return render(request, 'images/image/create.html', context={
        'section': 'images',
        'form': form
    })


@login_required
def image_detail(request, id: int, slug: str):
    # get the object
    image = get_object_or_404(Image, pk=id, slug=slug)
    return render(request, 'images/image/detail.html', {
        'image': image,
        'section': 'images',
        })


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({
        'status': 'error'
    })