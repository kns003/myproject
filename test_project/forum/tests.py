from django.test import TestCase
import datetime,logging
from forum.models import Thread,Comment
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)
                  
class HomeViewsTestCase(TestCase):
    def test_index(self):
        thread=Thread.objects.get(pk=1)
        self.assertEqual(thread.choice_set.get(pk=1).title,'Python')
        logger.debug('I am here')
        resp = self.client.post('/thread/1/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/thread/1/')
        self.assertEqual(thread.choice_set.get(pk=1).title,'Python')
        
    def test_bad_index(self):
      
      resp = self.client.post('/thread/1000000/')
      self.assertEqual(resp.status_code, 404)
