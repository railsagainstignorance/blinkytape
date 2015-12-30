# -*- coding: utf-8 -*-

"""BlinkyTape Python communication library.

  This code assumes stock serialLoop() in the firmware.

  Commands are issued in 3-byte blocks, with pixel data
  encoded in RGB triplets in range 0-254, sent sequentially
  and a triplet ending with a 255 causes the accumulated pixel
  data to display (a show command).

  Note that with the stock firmware changing the maximum brightness
  over serial communication is impossible.
"""

import serial
import os.path
import subprocess
import re
from time import sleep

# For Python3 support- always run strings through a bytes converter
import sys
if sys.version_info < (3,):
    def encode(x):
        return x
else:
    import codecs
    def encode(x):
        return codecs.latin_1_encode(x)[0]


class BlinkyTape(object):
    min_colour_val = 0
    max_colour_val = 254

    def __init__(self, port=None, ledCount=60, buffered=True):
        """Creates a BlinkyTape object and opens the port.

        Parameters:
          port
            Required, port name as accepted by PySerial library:
            http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial
            It is the same port name that is used in Arduino IDE.
            Ex.: COM5 (Windows), /dev/ttyACM0 (Linux).
          ledCount
            Optional, total number of LEDs to work with,
            defaults to 60 LEDs. The limit is enforced and an
            attempt to send more pixel data will throw an exception.
          buffered
            Optional, enabled by default. If enabled, will buffer
            pixel data until a show command is issued. If disabled,
            the data will be sent in byte triplets as expected by firmware,
            with immediate flush of the serial buffers (slower).

        """
        self.port = self.__identify_port(port)
        print "port=%s" % self.port
        self.ledCount = ledCount
        self.position = 0
        self.buffered = buffered
        self.buf = ""
        self.serial = serial.Serial(self.port, 115200)
        self.show()  # Flush any incomplete data

    def __identify_port(self, port=None):
        if port is not None:
            return port
        elif os.name == 'posix': # covers all *nix machines, including Linux?
            if not os.path.exists( '/dev/serial') or not os.path.exists('/dev/serial/by-id'):
                raise RuntimeError("Assuming this is a *nix machine, cannot find the device path for BlinkyTape via 'ls -l /dev/serial/by-id'. Is it connected?")
            ls_l_output = subprocess.check_output(['ls', '-l', '/dev/serial/by-id'])
            m = re.search( 'BlinkyTape\S+\s+->\s+\S+(/tty\S+)', ls_l_output)
            if m == None:
                raise RuntimeError("Assuming this is a *nix machine, cannot find the device path for BlinkyTape via 'ls -l /dev/serial/by-id'. Is it connected?")
            device_path = '/dev' + m.group(1)
            return device_path
        elif os.name == 'nt': # covers all windows machines?
            cmd = "wmic path Win32_SerialPort Where 'Caption like \"%" + "BlinkyTape%\"' Get DeviceID" # Clumsy, but can't work out how else to avoid %B going weird
            com_name_output = subprocess.check_output(cmd)
            m = re.search( '(COM\d+)', com_name_output)
            if m == None:
                raise RuntimeError("Assuming this is a Windows machine, cannot find a matching COM port for BlinkyTape. Is it connected?")
            com_name = m.group(1)
            return com_name
        else:
            raise RuntimeError("Cannot establish what kind OS is running, so don't know where to look for the BlinkyTape connection.")

    def send_list(self, colors):
        if len(colors) > self.ledCount:
            raise RuntimeError("Attempting to set pixel outside range!")
        for r, g, b in colors:
            self.sendPixel(r, g, b)
        self.show()

    def colour_chr(self, n):
        if n < self.min_colour_val:
            n = self.min_colour_val
        elif n > self.max_colour_val:
            n = self.max_colour_val
        return chr(n)

    def send_list(self, colors):
        data = ""
        for r, g, b in colors:
            data += self.colour_chr(r) + self.colour_chr(g) + self.colour_chr(b)
        self.serial.write(encode(data))
        self.show()

    def sendPixel(self, r, g, b):
        """Sends the next pixel data triplet in RGB format.

        Values are clamped to 0-254 automatically.

        Throws a RuntimeException if [ledCount] pixels are already set.
        """
        data = self.colour_chr(r) + self.colour_chr(g) + self.colour_chr(b)
        if self.position < self.ledCount:
            if self.buffered:
                self.buf += data
            else:
                self.serial.write(encode(data))
                self.serial.flush()
            self.position += 1
        else:
            raise RuntimeError("Attempting to set pixel outside range!")

    def show(self):
        """Sends the command(s) to display all accumulated pixel data.

        Resets the next pixel position to 0, flushes the serial buffer,
        and discards any accumulated responses from BlinkyTape.
        """
        control = chr(255)
        if self.buffered:
            # Fix an OS X specific bug where sending more than 383 bytes of data at once
            # hangs the BlinkyTape controller. Why this is???
            # TODO: Test me on other platforms
            CHUNK_SIZE = 300

            self.buf += control
            for i in range(0, len(self.buf), CHUNK_SIZE):
                self.serial.write(encode(self.buf[i:i+CHUNK_SIZE]))
                self.serial.flush()

            self.buf = ""
        else:
            self.serial.write(encode(control))
        self.serial.flush()
        self.serial.flushInput()  # Clear responses from BlinkyTape, if any
        self.position = 0

    def displayColor(self, r, g, b):
        """Fills [ledCount] pixels with RGB color and shows it."""
        for i in range(0, self.ledCount):
            self.sendPixel(r, g, b)
        self.show()

    def resetToBootloader(self):
        """Initiates a reset on BlinkyTape.

        Note that it will be disconnected.
        """
        self.serial.setBaudrate(1200)
        self.close()

    def close(self):
        """Safely closes the serial port."""
        self.serial.close()

    def clear_all(self):
        for x in range(self.ledCount):
            self.sendPixel(0, 0, 0)
        self.show()


# Example code

if __name__ == "__main__":

    import glob
    import optparse

    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="portname",
                      help="serial port (ex: /dev/ttyUSB0)", default=None)
    parser.add_option("-c", "--ledcount", dest="ledcount",
                      help="number of LEDs attached", type="int", default=60)
    parser.add_option("-b", action="store_true", default="True", dest="buffered")
    parser.add_option("-u", action="store_false", dest="buffered")

    (options, args) = parser.parse_args()

    bt = BlinkyTape(options.portname, options.ledcount, options.buffered)

    while True:
        bt.displayColor(255, 0, 0)
        sleep(0.5)
        bt.displayColor(0, 255, 0)
        sleep(0.5)
        bt.displayColor(0, 0, 255)
        sleep(0.5)
        bt.displayColor(255, 255, 255)
        sleep(0.5)
        bt.displayColor(0, 0, 0)
        sleep(0.5)
