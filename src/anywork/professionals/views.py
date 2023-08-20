from django.shortcuts import render, get_object_or_404, redirect
from .forms import RawProfessionalForm, ProfessionalForm
from .models import Professional

# Create your views here.
def professional_detail_view(request, id):
    obj = get_object_or_404(Professional, id=id)
    context = {
        'object': obj
    }
    return render(request, "professionals/professional_detail.html", context)

def professional_delete_view(request, id):
    obj = get_object_or_404(Professional, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("../../")
    context = {
        'object': obj
    }
    return render(request, "professionals/professional_delete.html", context)

def professional_create_view(request):
    my_form = RawProfessionalForm()
    if request.method == "POST":
        my_form = RawProfessionalForm(request.POST)
        if my_form.is_valid():
            Professional.objects.create(**my_form.cleaned_data)
            my_form = RawProfessionalForm()
            return redirect("../professional/success")
        else:
            print(my_form.errors)
    context = {
        'form': my_form
    }
    return render(request, "professionals/professional_create.html", context)

def professional_update_view(request, id=id):
    obj = get_object_or_404(Professional, id=id)
    form = ProfessionalForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("../../success/")
    context = {
        'form': form
    }
    return render(request, "professionals/professional_update.html", context)

def professional_success_view(request):
    context = {
        "success": "Successful"
    }
    return render(request, "professionals/professional_success.html", context)

def professional_list_view(request):
    queryset = Professional.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "professionals/professional_list.html", context)

def professional_service_view(request, service):
    queryset = Professional.objects.filter(service=service.capitalize())
    context = {
        'object_list': queryset
    }
    return render(request, "professionals/professional_service.html", context)