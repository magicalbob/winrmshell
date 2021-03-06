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

def process_command(s, c, w):
  if c == "exit":
    print("Bye!")
    sys.exit(0)

  new_command="cd %s ; %s" % (w, c)

  try:
    r = s.run_ps(new_command)
  
    o=str(r.std_out, 'utf-8')

    if len(o) == 0:
      o=str(r.std_err, 'utf-8')

    if len(o) == 0:
      if r.status_code > 0:
        print("OOPS! WinRM Status Code: %s" % (r.status_code))

    o=o.replace('\\r\\n', '\n')
    o=o.split('\\n')

    if c.split(' ')[0] == 'cd':
      w=c.replace('cd ','')
    else:
      for l in o:
        print(l.replace('\\\\','\\'))

    return(w)
  except Exception as e:
    print("OOPS! WinRM Exception: %s" % (e))

WINRM_HOST, WINRM_USER, WINRM_PASS = handle_args()

server_session = connect_to_server(WINRM_HOST, WINRM_USER, WINRM_PASS)

working_dir=str(server_session.run_cmd('cd').std_out,'utf-8').replace('\n','').replace('\r','')

command = ''
while True:
  old_command = command
  command = input('$ ')
  if command == '!':
    command = old_command

  if len(command) > 0:
    working_dir=process_command(server_session, command, working_dir)
