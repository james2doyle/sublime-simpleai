import unittest

from SimpleAI.plugin.api_client import AsyncSimpleAI
from http.client import HTTPConnection, HTTPSConnection


class TestGetConnectionClass(unittest.TestCase):
    def test_get_connection_class__default(self):
        connection_class = AsyncSimpleAI.get_connection_class(hostname="openrouter.ai")
        self.assertIsInstance(connection_class, HTTPConnection)
        self.assertEqual(connection_class.host, "openrouter.ai")
        self.assertEqual(connection_class.port, 443)

    def test_get_connection_class__include_port(self):
        connection_class = AsyncSimpleAI.get_connection_class(hostname="openrouter.ai:1234")
        self.assertIsInstance(connection_class, HTTPConnection)
        self.assertEqual(connection_class.host, "openrouter.ai")
        self.assertEqual(connection_class.port, 1234)

    def test_get_connection_class__with_https_prefix_no_port(self):
        connection_class = AsyncSimpleAI.get_connection_class(hostname="https://openrouter.ai")
        self.assertIsInstance(connection_class, HTTPSConnection)
        self.assertEqual(connection_class.host, "openrouter.ai")
        self.assertEqual(connection_class.port, 443)

    def test_get_connection_class__with_https_prefix(self):
        connection_class = AsyncSimpleAI.get_connection_class(hostname="https://openrouter.ai:8443")
        self.assertIsInstance(connection_class, HTTPSConnection)
        self.assertEqual(connection_class.host, "openrouter.ai")
        self.assertEqual(connection_class.port, 8443)

    def test_get_connection_class__with_http_prefix(self):
        connection_class = AsyncSimpleAI.get_connection_class(hostname="http://127.0.0.1:1234")
        self.assertIsInstance(connection_class, HTTPConnection)
        self.assertEqual(connection_class.host, "127.0.0.1")
        self.assertEqual(connection_class.port, 1234)


if __name__ == "__main__":
    unittest.main()
