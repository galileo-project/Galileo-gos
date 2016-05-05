import sys

def puts_raw(string, *args, **kwargs):
    sys.stdout.write(string, *args, **kwargs)
    sys.stdout.flush()

def puts(string, *args, **kwargs):
    puts_raw(string, *args, **kwargs)
    sys.stdout.write("\n")

def gets(string, *args, **kwargs):
    if string:
        puts_raw(string, *args, **kwargs)
    return sys.stdin.readline()

