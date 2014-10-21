#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys, smtplib, getpass, socket, subprocess, argparse, Queue
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

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

    from_address = getpass.getuser() + '@' + socket.gethostname()
    to_address   = args.to

    charset = "utf-8"
    subject = "Ntfy"
    text    = message
    
    msg = MIMEText(text.encode(charset), "plain", charset)
    msg["Subject"] = Header(subject, charset)
    msg["From"]    = args.fro
    msg["To"]      = to_address
    msg["Date"]    = formatdate(localtime=True)

    smtp = smtplib.SMTP(args.host, args.port)
    smtp.sendmail(from_address,to_address,msg.as_string())
    smtp.close()

if __name__ == "__main__":
    defaultFrom = getpass.getuser() + '@' + socket.gethostname()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-t', '--to', required=True, help='To address')
    parser.add_argument('-s', '--host', required=False, default='localhost', help='Host name')
    parser.add_argument('-p', '--port', required=False, default=25, help='Port number')
    parser.add_argument('-f', '--fro', required=False, default=defaultFrom, help='From address')
    parser.add_argument('-n', '--num', required=False, default=100, help='Number of lines of stdin included in e-mail')
    args = parser.parse_args()
    print args
    main(args)
