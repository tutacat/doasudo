#!/usr/bin/env python3
import os
import subprocess
import argparse

doas_exe = ""
proc = subprocess.run('which doas', capture_output=True)
if proc.returncode!=0:
    print(proc.stderr)
    exit(128)
else:
    doas_exe = proc.stdout

def parse_args(has_args=False):
        parser = argparse.ArgumentParser(
            prog='doasudo.py',
            description='Translate (most) of the sudo command to doas',
            epilog='do as sudo',
        )
        parser.add_argument('command', nargs="*")
        parser.add_argument('-S', '--stdin', '-n', '--non-interactive',
            help="Non interactive mode, fail if the matching rule doesn't have the nopass option.",
            action='store_true',
            )
        parser.add_argument('-s', '--shell',
            help="Execute the shell from SHELL or /etc/passwd.",
            action='store_true',
            )
        parser.add_argument('-u', '--user',
            help="Execute the command as user.  The default is root.",
            )
        parser.add_argument('-T', '--command-timeout',
            help="No-op for compatability.",
            action='store_true'
            )
        parser.add_argument('-K', '--remove-timestamp',
            help="Clear any persisted authentications from previous invocations, then immediately exit.",
            action='store_const',
            const=3,
            dest='timestamp',
        )
        parser.add_argument('-k', '--reset-timestamp',
            help="Like -K, but a supplied command will be executed.",
            action='store_const',
            const=1,
            dest='timestamp',
            )
        return parser.parse_args()

args = parse_args()

doas_args = []

if args.user:
    doas_args.extend(('-u',args.user))
if args.shell:
    doas_args.extend('-s')
if args.stdin:
    doas_args.extend('-n')
args.timestamp = args.timestamp or 0

if not args.timestamp^2 and args.command != None:
        subprocess.run((doas_exe,) + tuple(doas_args) + ('--',) + tuple(command) )

if args.timestamp^1:
        subprocess.run((doas_exe, '-L'))
