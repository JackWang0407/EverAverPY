import unittest
import os
import sys
from mock import patch
from gp.recipe.phantomjs import Recipe

PARTS_DIRECTORY = "this_is_a_dummy"


class TestPhantomjs(unittest.TestCase):

    def setUp(self):
        self.name = 'test'
        self.buildout = {
            'buildout': {
                'parts-directory': PARTS_DIRECTORY,
                'relative-paths': 'true',
                'version': '1.9.7'
            }
        }
        self.install_dir = os.path.join(PARTS_DIRECTORY, self.name)
        self.options = {}
        self.recipe = Recipe(self.buildout, self.name, self.options)

    def test_to_relative(self):
        """ _to_relative should generate a buildout relative path """
        test_path = os.path.join('mytest', 'me')
        absolute_test_path = os.path.join(self.install_dir, test_path)
        result = self.recipe._to_relative(absolute_test_path)
        assert result == "join(base, 'parts', '{0}', '{1}')".format(
            self.name,
            test_path
        )

    def test_get_relative_binary_dict(self):
        """ _get_relative_binary_dict should return a valid relative dictionary """
        binaries = {
            'phantomjs': os.path.join(self.install_dir, 'phantomFoo'),
            'casperjs': os.path.join(self.install_dir, 'casperBar')
        }
        result = self.recipe._get_relative_binary_dict(binaries)
        assert (result ==
                "{'casperjs': join(base, 'parts', 'test', 'casperBar'), 'phantomjs': join(base, 'parts', 'test', 'phantomFoo')}")

    def test_get_url_from_template(self):
        """ _get_url_from_template should return the proper url """
        url = None
        if sys.platform == 'darwin':
            url = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-macosx.zip'
        elif sys.platform.startswith('linux'):
            arch = 'x86_64' in os.uname() and 'x86_64' or 'i686'
            url = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-' + arch + '.tar.bz2'
        elif sys.platform.startswith('win'):
            url = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-windows.zip'
        if url:
            assert self.recipe._get_url_from_template() == url

    def test_generate_template_dict(self):
        """ _generate_template_dict should return the proper values """
        arch = 'x86_64' in os.uname() and 'x86_64' or 'i686'
        if sys.platform == 'darwin':
            assert self.recipe._generate_template_dict() == {
                'arch': arch,
                'phantom_platform': 'macosx',
                'phantom_extension': 'zip',
                'platform': 'darwin',
                'version': '1.9.7'
            }
        elif sys.platform.startswith('win'):
            assert self.recipe._generate_template_dict() == {
                'arch': arch,
                'phantom_platform': 'windows',
                'phantom_extension': 'zip',
                'platform': 'windows',
                'version': '1.9.7'
            }
        elif sys.platform.startswith('linux'):
            assert self.recipe._generate_template_dict() == {
                'arch': arch,
                'phantom_platform': 'linux-{0}'.format(arch),
                'phantom_extension': 'tar.bz2',
                'platform': 'linux',
                'version': '1.9.7'
            }
