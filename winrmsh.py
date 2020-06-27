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

WINRM_HOST, WINRM_USER, WINRM_PASS = handle_args()

s = winrm.Session(WINRM_HOST,auth=(WINRM_USER,WINRM_PASS))

r = s.run_cmd('ipconfig')

print(r.std_out)
