from django.shortcuts import render



# Create your views here.

def index(request):
    current_user = request.user

    if request.method == "POST":
        user_id_id = current_user.id
        email = request.POST.get('email')

        sub = newsletter(user_id_id = user_id_id, email=email)
        sub.save()
        print("Newsletter subbed")
    
    exists = ""
    if request.user.is_authenticated:
        if_exists= newsletter.objects.filter(user_id = current_user).count()

        if if_exists == 1:
            exists = "Yes"
        else:
            exists ="No"
    

    context={
        'current_user':current_user,
        'exists': exists,
    }
    return render(request,'home/index.html',context)