from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):

    def test_create_user(self):
        """Create and save a User successfully"""
        User = get_user_model()
        user = User.objects.create_user(
            username='foo', email='foo@user.com', password='123'
        )
        self.assertEqual(user.email, 'foo@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', email='', password='123')

    def test_create_superuser(self):
        """Create and save a SuperUser successfully"""
        User = get_user_model()
        admin_user = User.objects.create_superuser('root', 'super@user.com', 'toor')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='gronk', email='super@user.com', password='666', is_superuser=False
            )



# NOTE: next: создать работника, руководителя, проект
