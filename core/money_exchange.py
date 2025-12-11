# If your money-exchange-1.html template needs user-specific data like kyc or account details, use the version in account/views.py.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import KYC, Account
@login_required
def money_exchange(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your KYC.")
            return render("account:kyc-reg")
        
        account = Account.objects.get(user=request.user)

        context = {
            "kyc": kyc,
            "account": account,
        }
        return render(request, "account/money-exchange-1.html", context)
    else:
        messages.warning(request, "You need to login to access this page.")
        return render("userauths:sign-in")



# If the page is generic or independent of user data, the version in core/money_exchange.py is sufficient.

# from django.shortcuts import render, redirect
# from django.contrib import messages

# def money_exchange(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, "You need to log in to access this page.")
#         return redirect("userauths:sign-in")  # Redirect to the login page
#     return render(request, "core/money-exchange-1.html")  # Render the template

@login_required
def money_exchange_2(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except KYC.DoesNotExist:
            messages.warning(request, "You need to submit your KYC before proceeding.")
            return redirect("account:kyc-reg")
        
        account = Account.objects.get(user=request.user)

        # Add context data if needed
        context = {
            "kyc": kyc,
            "account": account,
        }
        return render(request, "account/money-exchange-2.html", context)
    else:
        messages.warning(request, "You need to log in to access this page.")
        return redirect("userauths:sign-in")


@login_required
def crypto_view(request):
    if request.user.is_authenticated:
        try:
            # Check if the user has submitted KYC
            kyc = KYC.objects.get(user=request.user)
        except KYC.DoesNotExist:
            messages.warning(request, "You need to submit your KYC before proceeding.")
            return redirect("account:kyc-reg")  # Replace with your KYC registration route name

        try:
            # Retrieve the user's account
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            messages.warning(request, "You need to set up an account before proceeding.")
            return redirect("account:sign-up")  # Replace with your account setup route name

        # Add context data for rendering the crypto page
        context = {
            "kyc": kyc,
            "account": account,
        }
        return render(request, "core/crypto.html", context)  # Replace with your template path
    else:
        messages.warning(request, "You need to log in to access this page.")
        return redirect("userauths:sign-in")  # Replace with your login route name
