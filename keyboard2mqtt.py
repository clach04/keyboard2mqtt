#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import os
import sys


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %r on %r' % (sys.version, sys.platform))

    return 0


if __name__ == "__main__":
    sys.exit(main())
