"""Upload Instagram posts exported by Instaloader to WordPress"""

import os
import re
import sys
from argparse import ArgumentParser, ArgumentTypeError, SUPPRESS
from configparser import ConfigParser
from typing import List, Optional

from . import __version__, Ig2wp

def main():
    parser = ArgumentParser(description=__doc__, add_help=False,
                            epilog="The complete documentation can be found at "
                                   "https://github.com/aderbique/ig2wp/.",
                            fromfile_prefix_chars='+')

    g_file = parser.add_argument_group('File Path Specification')
    g_file.add_argument('-d', '--directory', metavar='/path/to/directory',
                        help='The directory path where the files are located.')

    g_login = parser.add_argument_group('Connection (To upload to Wordpress)',
                                        'Instagram to Wordpress can login to Wordpress. This allows uploading media '
                                        'obtained using the instaloader program. Be sure to specify all parameters.')
    g_login.add_argument('-s', '--server', metavar='https://my-wordpress-blog.com',
                         help='Root URL of your Wordpress site.')                                        
    g_login.add_argument('-u', '--username', metavar='YOUR-USERNAME',
                         help='Login name (profile name) for your Wordpress account.')
    g_login.add_argument('-p', '--password', metavar='YOUR-PASSWORD',
                         help='Password for your WordPress account. Without this option, '
                              'you\'ll be prompted for your password interactively if '
                              'there is not yet a valid session file.')

    g_misc = parser.add_argument_group('Miscellaneous Options')
    g_misc.add_argument('-w', '--write', action='store_true', help='Write your config data to a file.')
    g_misc.add_argument('-h', '--help', action='help', help='Show this help message and exit.')
    g_misc.add_argument('--version', action='version', help='Show version number and exit.',
                        version=__version__)
    args = parser.parse_args()

    if args.write:
        config_object = ConfigParser()
        config_object["USERINFO"] = {
            "username": args.username,
            "password": args.password,
        }
        config_object["SERVERCONFIG"] = {
            "server": args.server
        }
        config_object["INSTALOADERDIR"] = {
            "directory": os.path.abspath(args.directory)
        }
        config_dir = "{}/.ig2wp".format(os.path.expanduser('~'))
        if not os.path.exists(config_dir):
            os.mkdir(config_dir, 0o700)
        with open('{}/config.ini'.format(config_dir), 'w') as conf:
            config_object.write(conf)
            print("Config file saved to {}/config.ini".format(config_dir))

    try:
        instance = Ig2wp(directory=args.directory, host=args.server, username=args.username, password=args.password)
        instance.main()
        #instance.close()
    except Exception as err:
        raise SystemExit("Fatal error: %s" % err) from err

if __name__ == "__main__":
    main()