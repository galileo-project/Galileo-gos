import sys

def puts_raw(string, *args, **kwargs):
    sys.stdout.write(string, *args, **kwargs)

def puts(string, *args, **kwargs):
    puts_raw(string, *args, **kwargs)
    sys.stdout.write("\n")

def gets(string, *args, **kwargs):
    if string:
        puts_raw(string)
    return sys.stdin.read()