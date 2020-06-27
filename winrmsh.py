#!/usr/bin/env python3

import sys, winrm

def handle_args():
  USAGE="Usage: %s {host} {user} {pass}" % (sys.argv[0])

  if len(sys.argv) != 4:
    print(USAGE)
    sys.exit(-1)

  WINRM_HOST=sys.argv[1]
  WINRM_USER=sys.argv[2]
  WINRM_PASS=sys.argv[3]

  return WINRM_HOST, WINRM_USER, WINRM_PASS

def connect_to_server(h, u, p):
  s = winrm.Session(h,auth=(u, p))

  return s

def process_command(s, c):
  if c == "exit":
    print("Bye!")
    sys.exit(0)

  r = s.run_cmd(c)
  
  o=str(r.std_out)
  o=o.replace('\\r\\n', '\n')
  o=o.split('\\n')

  for l in o:
    print(l.replace('\\\\','\\'))

WINRM_HOST, WINRM_USER, WINRM_PASS = handle_args()

server_session = connect_to_server(WINRM_HOST, WINRM_USER, WINRM_PASS)

while True:
  command = input('$ ')

  if len(command) > 0:
    process_command(server_session, command)
