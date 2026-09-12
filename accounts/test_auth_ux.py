"""Auth UX tests — login errors, signup validation, username check, password reset."""
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()


class AuthUXTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='SecurePass123!',
            first_name='Ex',
            last_name='isting',
        )

    def test_login_wrong_password_shows_error(self):
        res = self.client.post(reverse('login'), {
            'username': 'existing',
            'password': 'wrong-password',
        })
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Invalid username or password', status_code=200)

    def test_login_success(self):
        res = self.client.post(reverse('login'), {
            'username': 'existing',
            'password': 'SecurePass123!',
        }, follow=False)
        self.assertEqual(res.status_code, 302)

    def test_register_preserves_values_on_error(self):
        res = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'existing',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
        })
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'already taken')
        self.assertContains(res, 'value="New"')

    def test_check_username_available(self):
        res = self.client.get(reverse('check_username'), {'username': 'brandnew'})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['available'])

    def test_check_username_taken(self):
        res = self.client.get(reverse('check_username'), {'username': 'existing'})
        data = res.json()
        self.assertFalse(data['available'])

    def test_check_username_rejects_special_characters(self):
        res = self.client.get(reverse('check_username'), {'username': 'bad_user!'})
        data = res.json()
        self.assertFalse(data['available'])
        self.assertIn('letters and numbers', data['message'])

    def test_register_rejects_short_password(self):
        res = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser123',
            'email': 'newuser@example.com',
            'password1': 'abc',
        })
        self.assertEqual(res.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser123').exists())
        self.assertContains(res, 'at least 8 characters', status_code=200)

    def test_password_reset_requires_username_and_email(self):
        res = self.client.post(reverse('password_reset'), {
            'username': 'existing',
            'email': 'existing@example.com',
        })
        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_no_enumeration_on_mismatch(self):
        res = self.client.post(reverse('password_reset'), {
            'username': 'existing',
            'email': 'wrong@example.com',
        })
        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)
