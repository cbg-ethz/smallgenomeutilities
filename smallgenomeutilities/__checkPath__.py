#!/usr/bin/env python3

import os
import argparse


class CheckPath(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):

        path = values

        if not os.path.exists(path):
            os.makedirs(path)

        if os.access(path, os.W_OK):
            setattr(namespace, self.dest, path)
        else:
            raise argparse.ArgumentTypeError(
                "CheckPath:{0} is not a writable directory".format(path))
