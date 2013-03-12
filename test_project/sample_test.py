from django.test import TestCase
#from test_project import views

class HomeViewTestCase(TestCase):
    def test_home(self):
        response=self.client.get('/')
        self.assertEqual(response.status_code,200)
