# -*- coding: utf-8 -*-
"""
test_basic_logic
~~~~~~~~~~~~~~~~

Test the basic logic of the h2 state machines.
"""
import h2.connection
import h2.exceptions


class TestBasicClient(object):
    """
    Basic client-side tests.
    """
    example_request_headers = [
        (':authority', 'example.com'),
        (':path', '/'),
        (':scheme', 'https'),
        (':method', 'GET'),
    ]
    example_response_headers = [
        (':status', '200'),
        ('server', 'fake-serv/0.1.0')
    ]

    def test_begin_connection(self):
        c = h2.connection.H2Connection()
        events = c.initiate_connection()
        assert not events
        assert c.data_to_send.startswith(b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n')

    def test_sending_headers(self):
        c = h2.connection.H2Connection()
        c.initiate_connection()

        # Clear the data, then send headers.
        c.data_to_send = b''
        events = c.send_headers(1, self.example_request_headers)
        assert not events
        assert c.data_to_send == (
            b'\x00\x00\r\x01\x04\x00\x00\x00\x01'
            b'A\x88/\x91\xd3]\x05\\\x87\xa7\x84\x87\x82'
        )

    def test_sending_data(self):
        c = h2.connection.H2Connection()
        c.initiate_connection()
        c.send_headers(1, self.example_request_headers)

        # Clear the data, then send some data.
        c.data_to_send = b''
        events = c.send_data(1, b'some data')
        assert not events
        assert c.data_to_send == b'\x00\x00\t\x00\x00\x00\x00\x00\x01some data'
