__author__ = 'sdiemert'

import platform
import re
import serial  # usb serial interface.
import serial.tools
import serial.tools.list_ports
import struct
import Packet
from datetime import datetime


class SerialInterface:
    def __init__(self, view=None, portName=None):
        self.view = view
        self.port = portName
        self.conn = None
        self.data = []

    def set_view(self, v):
        self.view = v

    def output(self, message, level=1):
        if self.view:
            self.view.display_message(message, level)

    def get_available_serial_ports(self):

        to_return = list()
        for t in serial.tools.list_ports.comports():
            to_return.append(t[0])

        return to_return

    def add_data(self, d):
        self.data.append(d)

    def get_data(self):
        return self.data

    def store_packet_data(self,p):
        self.add_data(p.get_data())

    def _check_port(self, p):
        """
        Determines if the serial port name is valid for the given platform.
        :param p:
        :return bool: True if the port matches the OS type, False otherwise.
        """

        # Check the system type and if the port name matches the system type

        sys = platform.system()
        print self.get_available_serial_ports()

        if sys == "Windows":
            # Windows system, check that we are operating on COM ports
            # TODO: Update this to work on windows
            if re.search(".*COM.*", sys):
                # Check that the serial port we just validated actually exists.
                return p in self.get_available_serial_ports()
            else:
                return False

        elif sys == "Darwin" or sys == "Linux":

            print "System type determined to be Unix"

            # Mac or Linux, check that we have something in /dev/tty.*
            # TODO: Check this with a live source.

            if re.search("/dev/(cu|tty)\\..*", p):
                # Check that the serial port we just validated actually exists.
                return p in self.get_available_serial_ports()
        else:
            print "Could not find system type"
            return False

    def read_packet(self):

        # packet has 12 bytes.
        s = self.conn.read(12)

        if not s:
            print "read() returned :" + str(s) + ": returning None from read_packet()"
            return None

        x = None

        for c in s:
            print ord(c),

        print ""

        try:
            # Arduino uses Little Endian format
            # < in the fmt string of the unpack_from()
            # tells struct library to use little endian...
            x = struct.unpack_from("<bbbbbbbbI", s)
        except Exception as e:
            print "Unable to read packet! Error was: "
            print e
            return None

        p = Packet.TimePacket()

        p.seq = int(x[0])
        p.ack = int(x[1])
        p.type = int(x[2])
        p.action = int(x[3])
        p.min = int(x[4])
        p.hour = int(x[5])
        p.day = int(x[6])
        p.month = int(x[7])
        p.year = int(x[8])

        return p

    def send_packet(self, p):

        x = struct.pack("<bbbbbbbbI", p.seq, p.ack, p.type, p.action, p.min, p.hour, p.day, p.month, p.year)

        print "SENDING: "+str(p)

        self.output("SENDING: "+str(p))

        self.conn.write(x)

    def send_date(self):

        current_time = datetime.today()

        t = Packet.TimePacket()

        t.seq = 0
        t.ack = 0
        t.type = Packet.TIME
        t.action = 0
        t.min = current_time.minute
        t.hour = current_time.hour
        t.day = current_time.day
        t.month = current_time.month
        t.year = current_time.year

        self.send_packet(t)

    def connect(self, port):

        return_status = False

        if self._check_port(port):

            self.port = port

            print "Beginning protocol"
            self.output("Beginning communication protocol with Arduino")

            try:
                self.conn = serial.Serial(self.port, timeout=2)
                self.conn.write('$')

                p = self.read_packet()

                while p:

                    if not p:
                        print "received invalid packet!"
                        break

                    if not p.is_complete():
                        print "Received incomplete packet!"
                        break

                    print "RECEIVED: "+str(p)
                    self.output("RECEIVED: "+str(p))

                    if p.is_data():
                        self.store_packet_data(p)

                    if p.is_data_done():
                        print "Received data done packet!"
                        self.send_date()

                    if p.is_term():
                        print "Received termination packet! Ending communications..."
                        self.output("Received termination packet from Arduino. Completing communications")
                        return_status = True
                        break

                    p = self.read_packet()

                self.output("Completed communication with Arduino.", 1)
                self.conn.close()

            except OSError:
                print "Error cannot connect to device"
                self.output("Could not connect to Arduino on port: "+port, 2)
                return False
        else:
            print "port: " + port + " failed port check"
            self.output("Port: "+port+" is invalid! Try another one", 2)
            self.conn.close()
            return False

        return return_status

    def reset(self):
        self.conn = None
        self.data = []

if __name__ == '__main__':
    s = SerialInterface()
    s.connect("/dev/cu.usbserial-A403MS94")
