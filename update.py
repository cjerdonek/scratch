"""
Build-helper script.

"""

import datetime
import fnmatch
import logging
import os
import re
import sys

import yaml

from versioner import common
from versioner.common import execute_command
from versioner.tf import TF
from versioner import assemblyinfo


TF_PATH = r"C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\tf"
BRANCH_PATH = "C:/TFS/CJ2010/ChicagoApplicationDevelopment/Dev"
    

DEFAULT_LOGGING_LEVEL = logging.DEBUG
#DEFAULT_LOGGING_LEVEL = logging.INFO

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


def read(path):
    with open(path) as f:
        text = f.read()
    
    return text

def get_assembly_info_paths(root_path):

    paths = []
    for root, dirnames, filenames in os.walk(root_path):
        for filename in fnmatch.filter(filenames, 'AssemblyInfo.*'):
            path = os.path.join(root, filename)
            paths.append(path)

    return paths

def get_project_directory(info_path):
    dir_path = os.path.dirname(info_path)

    parent_dir, dir_name = os.path.split(dir_path)
    
    if dir_name.lower() in ('properties', 'my project'):
        return parent_dir

    return dir_path

def get_assembly_version(info_path):
    text = read(info_path)
    pattern = '^(?:\[assembly|<Assembly): AssemblyVersion\("(?P<version>.*)".*$'
    m = re.search(pattern, text, re.MULTILINE)
    return m.group('version')
    
def get_project_info(info_path):
    version = get_assembly_version(info_path)
    project_dir = get_project_directory(info_path)
    parent_dir, dir_name = os.path.split(project_dir)
    label = os.path.join(os.path.basename(parent_dir), dir_name)
    
    tf = TF(TF_PATH)
    changeset_number, date, comment_start = tf.get_most_recent_changeset_info(project_dir)
    return date, version, label


def make_new_version_number(date, changeset_number):
    year = int(str(date.year)[2:])
    version = "%d.%d.%d.%d" % (year, date.month, date.day, changeset_number)
    return version


class Processor(object):

    def __init__(self, tf_path):
        self.tf = TF(tf_path)

    def get_project_info(self, info_path):
        assembly_version = get_assembly_version(info_path)
        project_dir = get_project_directory(info_path)
        parent_dir, dir_name = os.path.split(project_dir)
        label = os.path.join(os.path.basename(parent_dir), dir_name)
        
        return project_dir, label, assembly_version

    def update_assembly_info(self, path, project_name, old_version, new_version):
        self.tf.checkout(path)
        text = read(path)
        updated_text = assemblyinfo.change_version(text, new_version)
        common.write(path, updated_text)

        comment = "[Versioning] Update %s from '%s' to '%s'." % (project_name, old_version, new_version)
        #self.tf.checkin(path, comment)

    def get_last_change(self, project_dir):
        """
        Return None if last change was versioning-related.
        
        """
        changeset_number, date, comment_start = self.tf.get_most_recent_changeset_info(project_dir)
        if comment_start.lower() == '[versioning]':
            return None

        return date, changeset_number
        
    def update_project(self, assembly_info_path):
        project_dir, project_label, assembly_version = self.get_project_info(assembly_info_path)
        last_change = self.get_last_change(project_dir)

        if last_change is None:
            _log.info("No changes: skipping: %s" % project_label)
            return
        
        date, changeset_number = last_change

        new_version = make_new_version_number(date, changeset_number)
        
        self.update_assembly_info(assembly_info_path, project_label, assembly_version, new_version)
        

def main(sys_argv):
    configure_logging(DEFAULT_LOGGING_LEVEL)

    processor = Processor(TF_PATH)

    info_paths = get_assembly_info_paths(BRANCH_PATH)
    
    for info_path in info_paths:
        processor.update_project(info_path)

    try:
        pass
        #monitors, options = parse_args(sys_argv, monitors)
    except ParsingError as e:
        exit_with_error(e)


if __name__ == '__main__':
    main(sys.argv)
