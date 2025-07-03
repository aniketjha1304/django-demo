from django.shortcuts import render, redirect
from django.contrib import messages
from .models import InquiryForm
from .forms import InquiryFormForm

# Create your views here.


def inquiry_form_view(request):
    """
    Function-based view to handle inquiry form submission
    """
    if request.method == "POST":
        form = InquiryFormForm(request.POST)
        if form.is_valid():
            # Save the form data
            form.save()
            messages.success(request, "Inquiry form submitted successfully!")
            return redirect("show_records")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InquiryFormForm()

    return render(request, "inquiry_app/form.html", {"form": form})


def show_records_view(request):
    """
    Function-based view to display all saved records
    """
    records = InquiryForm.objects.all().order_by("-created_at")
    return render(request, "inquiry_app/records.html", {"records": records})
