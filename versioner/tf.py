"""
Python wrappers for command-line tf commands.

"""

import datetime
import logging

from .common import execute_command

_log = logging.getLogger("tf")


def escape(text):
    if " " in text:
        return '"%s"' % text
    return text


class TF(object):

    def __init__(self, tf_path):
        self.tf_path = tf_path

    def execute_tf(self, cmd):
        cmd = '"%s" %s' % (self.tf_path, cmd)
        lines = execute_command(cmd)
        return lines
    
    def get_most_recent_changeset_info(self, path):
        cmd = 'history "%s" /recursive' % path

        lines = self.execute_tf(cmd)

        line = lines[2]
        parts = line.split()
        
        changeset_number = int(parts[0])
        date_string = parts[2]
        comment_start = parts[3]  

        month, day, year = map(int, date_string.split("/"))
        date = datetime.date(year, month, day)
    
        return changeset_number, date, comment_start

    def checkout(self, path):
        cmd = 'checkout %s' % escape(path)
        self.execute_tf(cmd)

    def checkin(self, path, comment):
        # We don't include the /noprompt option to allow manual review.
        cmd = 'checkin /comment:"%s" %s' % (comment, path)
        self.execute_tf(cmd)


        