from django.shortcuts import render
from store.models import Product, LGA
from greatKart.forms import PersonForm
from django.http import JsonResponse



def home(request):
    products = Product.objects.all().filter(is_available = True)
    context = {
        'products' : products
    }
    return render(request, 'home.html', context)




def test(request):
    form = PersonForm()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            form = PersonForm()  
            
    context = {
        'form': form
    }
    return render(request, 'test_templates/test.html', context)

def get_lgas(request, state_id):
    """AJAX view to return LGAs for a selected state"""
    lgas = LGA.objects.filter(state_id=state_id).order_by('name').values('id', 'name')
    return JsonResponse(list(lgas), safe=False)