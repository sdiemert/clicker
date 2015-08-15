__author__ = 'sdiemert'

import platform
import re
import os
import serial  # usb serial interface.
import serial.tools
import serial.tools.list_ports
import struct
import Packet


class SerialInterface:
    def __init__(self, portName=None):
        self.port = portName
        self.conn = None

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
        print self._get_available_serial_ports()

        if sys == "Windows":
            # Windows system, check that we are operating on COM ports
            # TODO: Update this to work on windows
            if re.search(".*COM.*", sys):
                # Check that the serial port we just validated actually exists.
                return p in self._get_available_serial_ports()
            else:
                return False

        elif sys == "Darwin" or sys == "Linux":

            print "System type determined to be Unix"

            # Mac or Linux, check that we have something in /dev/tty.*
            # TODO: Check this with a live source.

            if re.search("/dev/(cu|tty)\\..*", p):
                # Check that the serial port we just validated actually exists.
                return p in self._get_available_serial_ports()
        else:
            print "Could not find system type"
            return False

    def read_packet(self):

        # packet has 11 bytes.
        s = self.conn.read(11)

        if not s:
            print "read() returned :" + str(s) + ": returning None from read_packet()"
            return None

        x = None

        try:
            # Arduino uses Little Endian format
            # < in the fmt string of the unpack_from()
            # tells struct library to use little endian...
            x = struct.unpack_from("<bbbbbbbI", s)
            print x
        except:
            print "unable to read packet!"
            return None

        p = Packet.TimePacket()

        p.seq = int(x[0])
        p.ack = int(x[1])
        p.type = int(x[2])
        p.min = int(x[3])
        p.hour = int(x[4])
        p.day = int(x[5])
        p.month = int(x[6])
        p.year = int(x[7])

        return p

    def connect(self, port):

        if self._check_port(port):

            self.port = port

            self.conn = serial.Serial(self.port, timeout=2)
            self.conn.write('$')

            p = self.read_packet()

            while p:

                if not p:
                    print "received invalid packet!"
                    break

                if not p.is_complete():
                    print "Received in complete packet!"
                    break

                if p.is_term():
                    print "Received termination packet! Ending communications..."
                    break

                p = self.read_packet()

            self.conn.close()

        else:
            print "port: " + port + " failed port check"
            self.conn.close()
            return False


if __name__ == '__main__':
    s = SerialInterface()
    s.connect("/dev/cu.usbserial-A403MS94")
