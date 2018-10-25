# -*- coding: utf-8 -*-
"""Recipe phantomjs"""
import glob
import sys
import os

DEFAULT_URL_TEMPLATE = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-{version}-{phantom_platform}.{phantom_extension}'


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.install_dir = os.path.join(
            buildout['buildout']['parts-directory'], name
        )
        self.relative_paths = self.buildout['buildout'].get('relative-paths',
                                                            False)

    def get_version(self, options):
        version = options.get('phantomjs-version')
        if version:
            return version
        import pkg_resources
        version = pkg_resources.get_distribution('gp.recipe.phantomjs').version
        version = list(version.split('.'))[:3]
        return '.'.join(version)

    def get_binaries(self):
        binaries = glob.glob(os.path.join(self.install_dir, '*', 'bin', '*js'))
        if sys.platform.startswith('win'):
            binaries.extend(
                glob.glob(os.path.join(self.install_dir, '*', '*.exe')))
        rv = {}
        for p in binaries:
            bname = os.path.basename(p)
            if bname.lower().endswith('.js'):
                continue
            if bname.lower().endswith('.exe'):
                bname = bname[:-4]
            rv[bname] = p
        return rv

    def download(self, url):
        from hexagonit.recipe.download import Recipe as Download
        options = self.options
        options['url'] = url
        dl = Download(self.buildout, self.name, options)
        dl.install()

    def _get_url_from_base(self):
        version = self.get_version(self.options)
        url_base = self.options.get('phantomjs-url-base', None)
        if sys.platform.startswith('linux'):
            arch = 'x86_64' in os.uname() and 'x86_64' or 'i686'
            url = (
                '%s/phantomjs-%s-linux-%s.tar.bz2'
            ) % (url_base, version, arch)
        elif sys.platform == 'darwin':
            url = (
                '%s/phantomjs-%s-macosx.zip'
            ) % (url_base, version)
        elif sys.platform.startswith('win'):
            url = (
                '%s/phantomjs-%s-windows.zip'
            ) % (url_base, version)
        else:
            raise RuntimeError('Please specify a phantomjs-url')
        return url

    def _generate_template_dict(self):
        arch = 'x86_64' in os.uname() and 'x86_64' or 'i686'
        if sys.platform == 'darwin':
            phantom_platform = 'macosx'
            phantom_extension = 'zip'
            platform = 'darwin'
        elif sys.platform.startswith('win'):
            phantom_platform = 'windows'
            phantom_extension = 'zip'
            platform = 'windows'
        # else we assume linux
        elif sys.platform.startswith('linux'):
            phantom_platform = 'linux-{0}'.format(arch)
            phantom_extension = 'tar.bz2'
            platform = 'linux'
        else:
            raise RuntimeError('Please specify a phantomjs-url')

        return {
            'arch': arch,
            'phantom_platform': phantom_platform,
            'phantom_extension': phantom_extension,
            'platform': platform,
            'version': self.get_version(self.options)
        }

    def _get_url_from_template(self):
        template_dict = self._generate_template_dict()
        url_template = self.options.get('phantomjs-url-template', DEFAULT_URL_TEMPLATE)
        return url_template.format(**template_dict)

    def install(self):
        """Installer"""
        binaries = self.get_binaries()
        if 'phantomjs' not in binaries:
            if self.options.get('phantomjs-url', None):
                url = self.options.get('phantomjs-url')
            elif self.options.get('phantomjs-url-base', None):
                url = self._get_url_from_base()
            else:
                url = self._get_url_from_template()
            self.download(url)
        if 'casperjs' not in binaries:
            url = self.options.get(
                'casperjs-url',
                'https://github.com/n1k0/casperjs/tarball/1.0.3')
            if url:
                self.download(url)

        binaries = self.get_binaries()
        for f in binaries.values():
            os.chmod(f, 0o777)

        if self.relative_paths:
            self.options['arguments'] = \
                self._get_relative_binary_dict(binaries)
        else:
            self.options['arguments'] = repr(binaries)
        self.options['eggs'] = 'gp.recipe.phantomjs'
        self.options['entry-points'] = '\n'.join([
            '%s=gp.recipe.phantomjs.script:main' % s for s in binaries
        ])
        from zc.recipe.egg import Scripts
        rscripts = Scripts(self.buildout, self.name, self.options)
        return rscripts.install()

    update = install

    def _get_relative_binary_dict(self, binaries):
        """ convert absolute paths to relative arguments """
        dict_items = ("'{0}': {1}".format(name, self._to_relative(path))
                      for name, path in sorted(binaries.items()))
        return "{{{0}}}".format(", ".join(dict_items))

    def _to_relative(self, absolute_path):
        """ convert an absolute path to a relative one """
        path = absolute_path.replace(self.install_dir, '').lstrip(os.sep)
        return "join(base, 'parts', '{0}', '{1}')".format(self.name, path)
