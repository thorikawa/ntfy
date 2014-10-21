#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import time, sys

def main():
    for i in range(0, 20):
        print "message" + str(i)
        time.sleep(0.01)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
