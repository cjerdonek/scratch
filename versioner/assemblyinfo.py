"""
Supports parsing AssemblyInfo files.

"""

import logging
import re
import sys
import unittest


_log = logging.getLogger("assemblyinfo")


def change_version(text, new_version):
    """
    Change the assembly version in the contents of an AssemblyInfo file.

    """
    pattern = '^(?P<initial>(?:\[assembly|<Assembly): Assembly(?:File)?Version(?:Attribute)?\(")(?P<version>[^"]*)'
    repl = r'\g<initial>%s' % new_version
    text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    return text


class ChangeVersionTests(unittest.TestCase):

    def _assert_equals(self, expected, actual):
        message = """\

Expected:

-->%s<--
----
Actual:

-->%s<--
----
""" % (expected, actual)

        self.assertEquals(actual, expected, message)
    
    def test_change_version_vb(self):
        text = """\
' Comment
<Assembly: AssemblyVersion("12.1.2.0")> 
<Assembly: AssemblyFileVersion("12.1.23.0")>
<Assembly: AssemblyFileVersionAttribute("12.1.23.0")>
' Comment
"""
        expected = """\
' Comment
<Assembly: AssemblyVersion("1.2.3.4")> 
<Assembly: AssemblyFileVersion("1.2.3.4")>
<Assembly: AssemblyFileVersionAttribute("1.2.3.4")>
' Comment
"""
        actual = change_version(text, "1.2.3.4")
        self._assert_equals(expected, actual)

    def test_change_version_csharp(self):
        text = """\
// Comment
[assembly: AssemblyVersion("12.1.23.0")]
[assembly: AssemblyFileVersion("12.1.23.0")]
[assembly: AssemblyFileVersionAttribute("12.1.23.0")]
// Comment
"""
        expected = """\
// Comment
[assembly: AssemblyVersion("1.2.3.4")]
[assembly: AssemblyFileVersion("1.2.3.4")]
[assembly: AssemblyFileVersionAttribute("1.2.3.4")]
// Comment
"""
        actual = change_version(text, "1.2.3.4")
        self._assert_equals(expected, actual)


if __name__ == '__main__':
    unittest.main()
