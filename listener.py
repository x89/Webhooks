#!/usr/bin/env python

import re
import argparse
import os
import sys
import SocketServer

_PORT = 25256
_DIR = '/tmp/repo'
_GIT = '…'

parser = argparse.ArgumentParser(description='Github automatic pull script.')
parser.add_argument('-f', '--fork', action='store_true',
                    help="fork to background")
parser.add_argument('-k', '--kill', action='store_true',
                    help="kill the running instance of puller")
args = parser.parse_args()


class ListenServer(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(8196)
        print "A push arrived."
        try:
            os.chdir(_DIR)
        except:
            print "Cloning new repo in {dir}".format(_DIR.format(repo))
            os.chdir(_DIR)
            os.system('git clone {git} .'.format(git=_GIT))
        os.chdir(_DIR)
        os.system('git pull origin {0}'.format(repo))

if __name__ == "__main__":
    if args.kill:
        with open('puller.pid', 'r') as fh:
            pid = fh.read()
            s = os.system('kill {0}'.format(int(pid)))
            if s == 0:
                os.system('rm -f puller.pid')
        sys.exit(0)
    if args.fork:
        pid = os.fork()
        if pid:
            with open('puller.pid', 'w') as fh:
                fh.write(str(pid))
            sys.exit()
    HOST, PORT = "0.0.0.0", _PORT
    server = SocketServer.TCPServer((HOST, PORT), ListenServer)
    server.serve_forever()
