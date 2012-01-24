"""
Build-helper script.

"""

import datetime
import logging
import os
import shutil
import sys
import textwrap
import win32pipe

import yaml

TF_PATH = r"C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\tf"

# Global variables:
#
# OUTPUT_DIR:
#
# The top-level folder to which to write all output files.
#
# We recommend mapping this directory to a virtual directory in IIS so that
# output files can be browsed easily using a web browser.  In thiS case, the
# virtual directory should be configured to have "directory browsing" enabled.

DEFAULT_LOGGING_LEVEL = logging.DEBUG

YAML_CONFIG_PATH = "config.yaml"
NO_DATA_GIF_SOURCE_PATH = "no_data_found.gif"
NO_DATA_GIF_PATH = "zomg_no_data_found.gif"

CHART_SCALING_FACTOR = 1.25

_module_name = os.path.basename(sys.argv[0])
_log = logging.getLogger(_module_name)


class CustomFormatter(logging.Formatter):

    _formatter1 = logging.Formatter("[%(levelname)s] ")
    _formatter2 = logging.Formatter("%(name)s: %(message)s")

    def format(self, record):
        # If we want to adjust the padding between the level and the rest, we
        # can do that here.
        return self._formatter1.format(record) + self._formatter2.format(record) 

def configure_logging(logging_level):
    logger = logging.getLogger()  # the root logger.

    stream = sys.stderr
    handler = logging.StreamHandler(stream)
    formatter = CustomFormatter()
    handler.setFormatter(formatter)

    logger.setLevel(logging_level)
    logger.addHandler(handler)

    _log.debug("Debug logging enabled.")


def exit_with_error(message):
    _log.error(message)
    print "\nExecute the command with the --help or -h option for usage info."
    sys.exit(1)


def execute_command(cmd):
    """
    Execute a command-line command and return the screen output as a string.

    """
    print "Executing: %s" % repr(cmd)
    with win32pipe.popen(cmd) as f:
        lines = f.readlines()

    return lines

def execute_tfs(cmd):
    cmd = '"%s" %s' % (TF_PATH, cmd)
    lines = execute_command(cmd)
    return lines

def get_most_recent(path):
    cmd = 'history %s /recursive' % path
    lines = execute_tfs(cmd)
    line = lines[2]
    parts = line.split()
    
    changeset_number = parts[0]
    date_string = parts[2]
    month, day, year = map(int, date_string.split("/"))
    date = datetime.date(year, month, day)

    return changeset_number, date

def main(sys_argv):
    """
    Generate new monitor graphs for the user-provided date range.
    
    """
    configure_logging(DEFAULT_LOGGING_LEVEL)

    path = "C:\TFS\CJ2010\ChicagoApplicationDevelopment\dev"
    print get_most_recent(path)
    exit()
    #config = read_yaml_config(path=YAML_CONFIG_PATH)

    try:
        pass
        #monitors, options = parse_args(sys_argv, monitors)
    except ParsingError as e:
        exit_with_error(e)


if __name__ == '__main__':
    main(sys.argv)
