# -*- coding: utf-8 -*-
import os
import sys


def main(binaries):
    os.environ['PHANTOMJS_EXECUTABLE'] = binaries['phantomjs']
    script_name = os.path.basename(sys.argv[0])
    if sys.platform.startswith('win'):
        script_name = script_name.replace('-script.py', '')

    script = binaries[script_name]
    args = [script] + sys.argv[1:]
    os.execve(args[0], args, os.environ)
