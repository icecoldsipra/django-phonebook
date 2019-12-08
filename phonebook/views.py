from django.contrib.auth.decorators import login_required


@login_required()
def error_page(request):
    raise NotImplementedError("Ha! Fooled you...")