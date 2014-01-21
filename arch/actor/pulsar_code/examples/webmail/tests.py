'''Test twisted integration'''
from pulsar.apps.test import unittest

from .arch.actor.pulsar_code.examples.webmail.manage import twisted, mail_client


@unittest.skipUnless(twisted, 'Requires twisted and a config file')
class TestWebMail(unittest.TestCase):
    concurrency = 'thread'
    server = None

    def testMailCient(self):
        client = yield mail_client(self.cfg, timeout=5)
        self.assertTrue(client)
