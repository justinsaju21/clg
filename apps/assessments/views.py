from django.shortcuts import render

# Create your views here.
def mock_view(request):
    return render(request, 'base.html')
