from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from account.models import KYC, Account

@login_required
def recipients(request):
    # Explicit user authentication check
    if not request.user.is_authenticated:
        messages.warning(request, "You need to login to access this page.")
        return redirect("userauths:sign-in")  # Redirect to your login page

    # Check if the user has submitted KYC
    try:
        kyc = KYC.objects.get(user=request.user)
    except KYC.DoesNotExist:
        messages.warning(request, "You need to submit your KYC.")
        return redirect("account:kyc-reg")  # Redirect to KYC submission page

    # Fetch recipients
    try:
        recipients_list = request.user.recipients.all()  # Assuming a related name `recipients`
    except AttributeError:
        recipients_list = []
        messages.warning(request, "No recipients found!")

    context = {
        "recipients": recipients_list,
        "kyc": kyc,  # Pass KYC data to the context if needed
    }
    return render(request, "core/recipients.html", context)
