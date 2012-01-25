"""
Supports executing command-line commands.

"""

import logging
import win32pipe


_log = logging.getLogger("optionparser")


def write(path, text):
    with open(path, "w") as f:
        f.write(text)

def execute_command(cmd):
    """
    Execute a command-line command and return the screen output as a string.

    """
    _log.debug("Executing: %s" % repr(cmd))
    
    cmd = """\
@echo OFF
%s
""" % cmd

    write('temp.bat', cmd)

    with win32pipe.popen('temp.bat') as f:
        lines = f.readlines()

    print "Output: %s" % "".join(lines)
    return lines
