from allauth.account.adapter import DefaultAccountAdapter
# from django.contrib import messages


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        # messages.success(request, f"Welcome {request.user.first_name}. Please sign in to access your account.")
        return "/contacts/home"
