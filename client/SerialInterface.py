__author__ = 'sdiemert'

import platform
import re
import os
import serial # usb serial interface.

class SerialInterface:

    def __init__(self):
        self.port = None

    def _get_available_serial_ports(self):

        to_return = list()
        for t in serial.tools.list_ports.comports():
            to_return.append(t[0])

        return to_return

    def _check_port(self, p):
        """
        Determines if the serial port name is valid for the given platform.
        :param p:
        :return bool: True if the port matches the OS type, False otherwise.
        """

        # Check the system type and if the port name matches the system type

        sys = platform.system()

        if sys == "Windows":
            # Windows system, check that we are operating on COM ports
            # TODO: Update this to work on windows
            if re.search(".*COM.*", sys):
                # Check that the serial port we just validated actually exists.
                return p in self._get_available_serial_ports()
            else:
                return False

        elif sys == "Darwin" or sys == "Linux":
            # Mac or Linux, check that we have something in /dev/tty.*
            # TODO: Check this with a live source.
            if re.search("/dev/tty\\.*", sys):
                # Check that the serial port we just validated actually exists.
                return p in self._get_available_serial_ports()
        else:
            return False

    def connect(self, port):
        if self._check_port(port):
            pass
        else:
            pass
