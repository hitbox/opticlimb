import argparse

import requests

production_authentication_url = 'https://www.opti-climb.com/{trigram}/ws/login/basic'

def main(argv=None):
    parser = argparse.ArgumentParser()
    args = parser.parse_args(argv)

if __name__ == '__main__':
    main()
