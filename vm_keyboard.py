#!/usr/bin/python

"""Send actions to Virtual machine.

This module has a VM class to manage it via keystrockes. It can be used to
automate tasks.

Key documentation:
Each key scancode requires a release key. This key is calculated by adding 0x80
to the key.

For example:

13 (R) + 0x80 = 0x93 (R-Release)
"""

import logging
import os

__author__ = 'twitter.com/entdark_'

logging.basicConfig(level=logging.DEBUG)
_VBOXMANAGE_PATH = '/usr/local/bin/VBoxManage'
class VM(object):
  """This class manages keystrokes in virtual machines."""

  def __init__(self, identifier):
    self.identifier = identifier

  def input_string(self, input_string):
    """Send a string to the VM."""
    logging.info('[+] Sending string {%s}', input_string)
    os.system('%s controlvm %s keyboardputstring %s' %
              (_VBOXMANAGE_PATH, self.identifier, input_string))

  def input_command(self, scan_code):
    """Send scan codes to VirtualBox."""
    logging.info('[+] Sending command {%s}', scan_code)
    os.system('%s controlvm %s keyboardputscancode %s' %
              (_VBOXMANAGE_PATH, self.identifier, scan_code))

  def input_scan_codes(self, scan_codes):
    """Send 2 or more scan codes separated by spaces and generate releases."""
    release = lambda c: str(hex(c + 0x80))

    scan_codes = scan_codes.split(' ')
    release_codes = [release(int(code, 16)) for code in scan_codes]

    scan_codes.extend(release_codes)

    # Remove 0x from list items because VBoxManage doesn't like it.
    scan_codes = [x.replace('0x', '') for x in scan_codes]
    self.input_command(' '.join(scan_codes))

  def enter(self):
    """Send Enter command."""
    self.input_command('1c 9c')

  def space(self):
    """Semd command."""
    self.input_command('39 b9')

  def quote(self):
    """Semd command."""
    self.input_command('2a 28 aa a8')

  def semicolon(self):
    """Semd command."""
    self.input_command('27 a7')

  def windows(self):
    self.input_command('e0 5b 13 93 e0 db')


# Example code to open cmd.exe and open a website.
if __name__ == '__main__':
  my_vm = VM('your-vm-name-here')
  my_vm.windows()
  my_vm.input_string('cmd.exe')
  my_vm.enter()
  my_vm.input_string('exit')
  my_vm.enter()
  my_vm.windows()
  my_vm.input_string('iexplore.exe www.wikipedia.org')
  my_vm.enter()
