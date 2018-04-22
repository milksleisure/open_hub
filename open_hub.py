#!/usr/bin/env python
import pyperclip
import os
import urllib.parse as parse
import glob
import subprocess
import argparse
import time
import re
from pykeyboard import PyKeyboard

GVFS='/run/user/1000/gvfs'

def send_copy():
    if False:
        # Currently won't do...
        time.sleep(0.2)
        k = PyKeyboard()
        k.press_key(k.control_key)
        k.tap_key('C')
        k.release_key(k.control_key)
        with open('/tmp/log', 'a') as wfd:
            wfd.write('Go!\n')
    subprocess.call(['xte', 'sleep 1', 'keydown Control_L', 'keydown C',
        'usleep 100', 'keyup Control_L', 'keyup C'])

def get_clipboard():
    return pyperclip.paste()

def parse_samba():
    url = get_clipboard()
    if 'smb://' not in url:
        print('No match smb...')
        return url

    url = parse.unquote(url)
    token = url.split('/')
    server = token[2]
    share = token[3]
    match = None
    pattern = re.compile('smb-share:server=([^,]+),share=([^,]+)')
    for i in glob.glob('{}/smb-share*'.format(GVFS)):
        result = pattern.search(i)
        if server == result.group(1) and share == result.group(2):
            match = i
            break

    if match is not None:
        path = url.replace('smb://{}/{}'.format(server,share),match)
        # TODO: fix more special paths
        return path

    # Shall not be here...
    return url


def get_options():
    parser = argparse.ArgumentParser(description='fast launcher via clipboard data')
    parser.add_argument('--play', action='store_true', help='Play the link')
    parser.add_argument('--view', action='store_true', help='View the link')
    parser.add_argument('--stream', action='store_true', help='Stream the link')
    return parser.parse_args()

def play_main():
    f = parse_samba()
    subprocess.call(['vlc', f])

def view_main():
    f = parse_samba()
    subprocess.call(['mcomix', f])

def stream_main():
    f = get_clipboard()
    subprocess.call(['streamlink', '-p', 'vlc', f, '1080p60,1080p,720p60,720p'])
    

if __name__ == '__main__':
    args = get_options()
    if args.play:
        send_copy()
        play_main()
    elif args.view:
        send_copy()
        view_main()
    elif args.stream:
        stream_main()
