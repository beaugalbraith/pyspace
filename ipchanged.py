#!/usr/bin/python3

""" 
based on https://github.com/davidiw/Grid-Appliance/blob/master/scripts/ip_monitor.py
structure info: http://man7.org/linux/man-pages/man7/rtnetlink.7.html

This application gathers the local machines IP Addresses and their matching
labels.  Thereafter, it will notify, via callback, any IP address changes. """

import socket, struct, threading, notify2

"""4 byte alignment"""
def align(inc):
  diff = inc % 4
  return inc + ((4 - diff) % 4)

class ifaddr:
  """Parse an ifaddr packet"""
  LOCAL = 2 # local ip address
  LABEL = 3 # interface

  def __init__(self, packet):
    self.family, self.prefixlen, self.flags, self.scope, self.index = \
        struct.unpack("BBBBI", packet[:8])

class rtattr:
  """Parse a rtattr packet"""
  GRP_IPV4_IFADDR = 0x10

  NEWADDR = 20
  DELADDR = 21
  GETADDR = 22

  def __init__(self, packet):
    self.len, self.type = struct.unpack("HH", packet[:4])
    if self.type == ifaddr.LOCAL:
      addr = struct.unpack("BBBB", packet[4:self.len])
      self.payload = "%s.%s.%s.%s" % (addr[0], addr[1], addr[2], addr[3])
    elif self.type == ifaddr.LABEL:
      self.payload = packet[4:self.len].strip("\0")
    else:
      self.payload = packet[4:self.len]

class netlink:
  """Parse a netlink packet"""
  REQUEST = 1
  ROOT = 0x100
  MATCH = 0x200
  DONE = 3

  def __init__(self, packet):
    self.msglen, self.msgtype, self.flags, self.seq, self.pid = \
        struct.unpack("IHHII", packet[:16])
    self.ifa = None
    try:
      self.ifa = ifaddr(packet[16:24])
    except:
      return

    self.rtas = {}
    pos = 24
    while pos < self.msglen:
      try:
        rta = rtattr(packet[pos:])
      except:
        break
      pos += align(rta.len)
      self.rtas[rta.type] = rta.payload

class ip_monitor:
  def __init__(self, callback = None):
    if callback == None:
      callback = self.notify
    self._callback = callback

  def print_cb(self, label, addr):
    print(label + " => " + addr)

  def notify(self, label, addr):
  	notify2.init("test")
  	notify2.Notification(label, addr).show()

  def request_addrs(self, sock):
    sock.send(struct.pack("IHHIIBBBBI", 24, rtattr.GETADDR, \
      netlink.REQUEST | netlink.ROOT | netlink.MATCH, 0, sock.getsockname()[0], \
      socket.AF_INET, 0, 0, 0, 0))

  def start_thread(self):
    threading.Thread.start(self.run, ())

  def run(self):
    sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, socket.NETLINK_ROUTE)
    sock.bind((0, rtattr.GRP_IPV4_IFADDR))
    self.request_addrs(sock)

    while True:
      data = sock.recv(4096)
      pos = 0
      while pos < len(data):
        nl = netlink(data[pos:])
        if nl.msgtype == netlink.DONE:
          break
        pos += align(nl.msglen)
        if nl.msgtype == rtattr.NEWADDR:
          self._callback(nl.rtas[ifaddr.LABEL], nl.rtas[ifaddr.LOCAL])
        if nl.msgtype == rtattr.DELADDR:
          self._callback(nl.rtas[ifaddr.LABEL], "Deleted: " + nl.rtas[ifaddr.LOCAL])

if __name__ == "__main__":
  ip_monitor().run()

"""
Traceback (most recent call last):
  File "ipchanges.py", line 104, in <module>
    ip_monitor().run()
  File "ipchanges.py", line 101, in run
    self._callback(nl.rtas[ifaddr.LABEL], nl.rtas[ifaddr.LOCAL])
KeyError: 3
"""
