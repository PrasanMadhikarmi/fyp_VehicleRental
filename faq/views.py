from django.shortcuts import render

# Create your views here.
def faq_index(request):
    context={

    }
    return render(request, 'faq/faq.html',context)
