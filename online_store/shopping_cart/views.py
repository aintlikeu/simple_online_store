from django.shortcuts import render


def example_view(request):
    return render(request, 'shopping_cart/example.html')
