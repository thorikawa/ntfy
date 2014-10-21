#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys, argparse, json, requests, Queue

def main(args):
    q = Queue.Queue(args.num)

    for line in sys.stdin:
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

    payload = {'text': message, 'username': args.name}
    r = requests.post(args.url, data=json.dumps(payload))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Notify to slack.')
    parser.add_argument('-u', '--url', required=True, help='Web hook url')
    parser.add_argument('-t', '--to', required=False, help='To user name')
    parser.add_argument('-n', '--num', required=False, default=100, help='Number of lines of stdin included in e-mail')
    parser.add_argument('-f', '--name', required=False, default='ntfy bot', help='Name shown on slack')
    args = parser.parse_args()
    print args
    main(args)
