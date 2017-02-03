# -*- coding: utf-8 -*-
"""Watchmaker cli."""
import argparse
import os
import sys

import watchmaker

from watchmaker import Prepare
from watchmaker.logger import prepare_logging


def _validate_log_dir(log_dir):
    if os.path.isfile(log_dir):
        raise argparse.ArgumentTypeError(
            '"{0}" exists as a file.'.format(log_dir)
        )
    return log_dir


def main():
    """Entry point for Watchmaker cli."""
    version_string = 'watchmaker v{0}'.format(watchmaker.__version__)
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=version_string,
                        help='Print version info.')
    parser.add_argument('--noreboot', dest='noreboot', action='store_true',
                        help='No reboot after provisioning.')
    parser.add_argument('--sourceiss3bucket', dest='sourceiss3bucket',
                        action='store_const', const=True, default=None,
                        help=(
                            'Use S3 buckets instead of internet locations for '
                            'files.'
                        ))
    parser.add_argument('--config', dest='config', default=None,
                        help='Path or URL to the config.yaml file.')
    parser.add_argument('--saltstates', dest='saltstates', default=None,
                        help=(
                            'Define the saltstates to use.  Must be None, '
                            'Highstate, or a comma-separated-string'
                        ))
    parser.add_argument('--log-dir', dest='log_dir', default=None,
                        type=_validate_log_dir,
                        help='Path to the log directory for logging.'
                        )
    parser.add_argument('-v', action='count', dest='verbosity', default=0,
                        help=(
                            'Enable verbose logging: -v for INFO, -vv to '
                            'include DEBUG, if option is left out, only '
                            'WARNINGS and higher are logged.'
                        ))

    arguments = parser.parse_args()
    prepare_logging(arguments.log_dir, arguments.verbosity)

    systemprep = Prepare(arguments)
    sys.exit(systemprep.install_system())
