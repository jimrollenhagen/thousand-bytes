import json
import unittest

from thousand_bytes.app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        super(AppTestCase, self).setUp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.img = open('images/world-map.png', 'rb')

    def tearDown(self):
        super(AppTestCase, self).tearDown()
        self.img.close()

    def test_convert_with_get(self):
        resp = self.app.get('/ascii')
        self.assertEqual(405, resp.status_code)

    def test_convert_no_image(self):
        resp = self.app.post('/ascii')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(400, resp.status_code)
        self.assertIn('error', data)
        self.assertEqual('must provide image to convert', data['error'])

    def test_convert_bad_image(self):
        with open('README.rst', 'rb') as f:
            resp = self.app.post('/ascii',
                                 data={'image': f})
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(400, resp.status_code)
        self.assertIn('error', data)
        self.assertEqual('invalid image', data['error'])

    def test_convert_string_height(self):
        resp = self.app.post('/ascii',
                             data={'height': 'foo', 'image': self.img})
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(400, resp.status_code)
        self.assertIn('error', data)
        self.assertEqual('"height" parameter must be a positive integer',
                         data['error'])

    def test_convert_negative_height(self):
        resp = self.app.post('/ascii',
                             data={'height': '-1', 'image': self.img})
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(400, resp.status_code)
        self.assertIn('error', data)
        self.assertEqual('"height" parameter must be a positive integer',
                         data['error'])

    def test_convert_zero_height(self):
        resp = self.app.post('/ascii',
                             data={'height': '0', 'image': self.img})
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(400, resp.status_code)
        self.assertIn('error', data)
        self.assertEqual('"height" parameter must be a positive integer',
                         data['error'])

    def test_convert_with_height(self):
        resp = self.app.post('/ascii',
                             data={'image': self.img, 'height': '30'})
        lines = resp.data.splitlines()
        line_length = len(lines[0])
        self.assertIn('text/plain', resp.content_type)
        self.assertEqual(30, len(lines))
        # ensure all lines are equal width
        for line in lines:
            self.assertEqual(line_length, len(line))

    def test_convert_default_height(self):
        resp = self.app.post('/ascii', data={'image': self.img})
        lines = resp.data.splitlines()
        line_length = len(lines[0])
        self.assertIn('text/plain', resp.content_type)
        self.assertEqual(50, len(lines))
        # ensure all lines are equal width
        for line in lines:
            self.assertEqual(line_length, len(line))
