from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import (
    UserLoginView, UserLogoutView, UserRegisterView, users_activate, UserUpdateView, UserPasswordResetView,
    UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView
)
from contacts.views import (
    ContactListView, ContactCreateView, ContactDetailView, ContactUpdateView, ContactDeleteView, contacts_home,
    contacts_about
)


class TestUsersUrls(SimpleTestCase):
    def test_users_login(self):
        url = reverse('users-login')
        self.assertEquals(resolve(url).func.view_class, UserLoginView)
        print("users-login test completed.")

    def test_users_logout(self):
        url = reverse('users-logout')
        self.assertEquals(resolve(url).func.view_class, UserLogoutView)
        print("'users-logout' test completed.")

    def test_users_register(self):
        url = reverse('users-register')
        self.assertEquals(resolve(url).func.view_class, UserRegisterView)
        print("users-register test completed.")

    def test_users_activate(self):
        url = reverse('users-activate', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func, users_activate)
        print("users-activate test completed.")

    def test_users_profile(self):
        url = reverse('users-profile', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, UserUpdateView)
        print("users-profile test completed.")

    def test_password_reset(self):
        url = reverse('password-reset')
        self.assertEquals(resolve(url).func.view_class, UserPasswordResetView)
        print("password-reset test completed.")

    def test_password_reset_done(self):
        url = reverse('password-reset-done')
        self.assertEquals(resolve(url).func.view_class, UserPasswordResetDoneView)
        print("password-reset-done test completed.")

    def test_password_reset_confirm(self):
        url = reverse('password-reset-confirm', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func.view_class, UserPasswordResetConfirmView)
        print("password-reset-confirm test completed.")

    def test_password_reset_complete(self):
        url = reverse('password-reset-complete')
        self.assertEquals(resolve(url).func.view_class, UserPasswordResetCompleteView)
        print("password-reset-complete test completed.")


class TestContactsUrls(SimpleTestCase):
    def test_contacts_home(self):
        url = reverse('contacts-home')
        self.assertEquals(resolve(url).func, contacts_home)
        print("contacts-home test completed.")

    def test_contacts_add(self):
        url = reverse('contacts-add')
        self.assertEquals(resolve(url).func.view_class, ContactCreateView)
        print("contacts-add test completed.")

    def test_contacts_browse(self):
        url = reverse('contacts-browse')
        self.assertEquals(resolve(url).func.view_class, ContactListView)
        print("contacts-browse test completed.")

    def test_contacts_view(self):
        url = reverse('contacts-view', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, ContactDetailView)
        print("contacts-view test completed.")

    def test_contacts_update(self):
        url = reverse('contacts-update', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, ContactUpdateView)
        print("contacts-update test completed.")

    def test_contacts_delete(self):
        url = reverse('contacts-delete', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, ContactDeleteView)
        print("contacts-delete test completed.")

    def test_contacts_about(self):
        url = reverse('contacts-about')
        self.assertEquals(resolve(url).func, contacts_about)
        print("contacts-about test completed.")
