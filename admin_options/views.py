from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from contacts.models import Contact
from users.models import CustomUser, LoggedInUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
@login_required
def admin_home(request):
    return render(request, 'admin_options/admin_options_home.html')


# To add a new contact to database
class AdminContactCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Contact
    template_name = 'contacts/contacts_add.html'
    success_message = "Contact %(first_name)s was added successfully."
    success_url = reverse_lazy('admin-contacts-browse')
    fields = ['first_name', 'last_name', 'email', 'mobile', 'city', 'birthday', 'image', 'added_by']


# To display all contacts in the database. Visible only to staff or admin
class AdminContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'admin_options/admin_contacts_browse.html'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_admin:
            return Contact.objects.all().order_by('-date_added')


# To view all details of a single contact
class AdminContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'admin_options/admin_contacts_view.html'
    # permission_required = ('admin_options.can_view', )


class LoggedInUserListView(LoginRequiredMixin, ListView):
    model = LoggedInUser
    template_name = 'admin_options/admin_loggedinusers.html'


class LoggedInUserDeleteView(LoginRequiredMixin, DeleteView):
    model = LoggedInUser
    template_name = 'contacts/contacts_delete.html'
    success_message = "User logged out successfully."
    success_url = reverse_lazy('admin-loggedinuser')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


class UserAccessReviewView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'admin_options/admin_useraccessreview.html'
    fields = ['email', 'is_active', 'is_staff', 'is_admin']
    success_message = "Profile updated successfully."
