#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys, argparse, json, requests, Queue

def main(args):
    q = Queue.Queue(args.num)

    for line in sys.stdin:
        if args.echo:
            sys.stdout.write(line)
            sys.stdout.flush()
        if q.full():
            q.get()
        q.put(line)

    message = ""
    while not q.empty():
        line = q.get()
        message = message + line

    if args.to:
        message = '@' + args.to + ' ' + message

    payload = {'text': message, 'username': args.name, 'icon_url': ''}

    if args.to:
        payload['link_names'] = 1

    r = requests.post(args.url, data=json.dumps(payload))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Notify to slack.')
    parser.add_argument('-u', '--url', required=True, help='Web hook url')
    parser.add_argument('-t', '--to', required=False, help='To user name')
    parser.add_argument('-n', '--num', required=False, default=100, help='Number of lines of stdin included in e-mail')
    parser.add_argument('-f', '--name', required=False, default='ntfy bot', help='Name shown on slack')
    parser.add_argument('-e', '--echo', action='store_true', help='Turn on echo back')
    parser.add_argument('-i', '--icon', required=False, default='http://thorikawa.github.io/ntfy/icon_128.png', help='Icon URL')
    parser.add_argument('-m', '--message', required=False, help='Send the given message instead of stdin')
    args = parser.parse_args()
    main(args)
