from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Contact
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


@login_required
def contacts_home(request):
    if request.user.is_authenticated:
        return render(request, 'contacts/contacts_home.html')


# To display all contacts in the database specific to logged in user
class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/contacts_browse.html'

    def get_queryset(self):
        return Contact.objects.filter(added_by=self.request.user).order_by('-date_added')


# To add a new contact to database
class ContactCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Contact
    template_name = 'contacts/contacts_add.html'
    success_message = "Contact %(first_name)s was added successfully."
    success_url = reverse_lazy('contacts-browse')
    fields = ['first_name', 'last_name', 'email', 'mobile', 'city', 'birthday', 'image']

    def form_valid(self, form):
        form.instance.added_by = self.request.user

        subject = f"Phonebook | New Contact Added | {form.instance.get_full_name()}"
        to = self.request.user
        from_email = settings.EMAIL_HOST_USER
        body = render_to_string('contacts/contact_add_email.html', {
            'first_name': form.instance.first_name,
            'last_name': form.instance.last_name,
            'email': form.instance.email,
            'mobile': form.instance.mobile,
            'city': form.instance.city,
            'birthday': form.instance.birthday,
            'image': form.instance.image.url,
            'date_added': form.instance.date_added,
        })

        # Send email to registered user
        send_email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to]
        )

        send_email.content_subtype = "html"
        send_email.send(fail_silently=False)

        return super().form_valid(form)


# To view all details of a single contact
class ContactDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Contact
    template_name = 'contacts/contacts_view.html'

    def test_func(self):
        value = self.get_object()
        if self.request.user == value.added_by:
            return True
        return False


# To update a contact from database
class ContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    template_name = 'contacts/contacts_update.html'
    success_message = 'Contact %(first_name)s was updated successfully'
    fields = ['first_name', 'last_name', 'email', 'mobile', 'city', 'birthday', 'image']

    def test_func(self):
        value = self.get_object()
        if self.request.user == value.added_by:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('contacts-view', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        form.instance.date_updated = timezone.now()

        subject = f"Phonebook | Contact Updated | {form.instance.get_full_name()}"
        to = self.request.user
        from_email = settings.EMAIL_HOST_USER
        body = render_to_string('contacts/contact_update_email.html', {
            'first_name': form.instance.first_name,
            'last_name': form.instance.last_name,
            'email': form.instance.email,
            'mobile': form.instance.mobile,
            'city': form.instance.city,
            'birthday': form.instance.birthday,
            'image': form.instance.image.url,
            'date_added': form.instance.date_added,
            'date_updated': form.instance.date_updated,
        })

        # Send email to registered user
        send_email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to]
        )
        send_email.content_subtype = "html"
        send_email.send(fail_silently=False)

        return super().form_valid(form)


# To delete a new contact to database
class ContactDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Contact
    template_name = 'contacts/contacts_delete.html'
    success_message = "Contact deleted successfully."
    success_url = reverse_lazy('contacts-browse')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)

        subject = f"Phonebook | Contact Deleted | {obj.get_full_name()}"
        to = self.request.user
        from_email = settings.EMAIL_HOST_USER
        body = render_to_string('contacts/contact_delete_email.html', {
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'email': obj.email,
            'mobile': obj.mobile,
            'city': obj.city,
            'birthday': obj.birthday,
            'image': obj.image.url,
            'date_added': obj.date_added,
            'date_updated': obj.date_updated,
        })

        # Send email to registered user
        send_email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to]
        )
        send_email.content_subtype = "html"
        send_email.send(fail_silently=False)

        return super().delete(request, *args, **kwargs)

    # To ensure that only the logged in user has access to his content
    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.added_by:
            return True
        return False


def contacts_about(request):
    return render(request, 'contacts/contacts_about.html')
