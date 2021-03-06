#!/usr/bin/python3
import termios 
import os 
import fcntl 
import json  
import struct 
import sys
import subprocess
import argparse
import datetime


uart_table = { "8250": 1, "16450":2, "16550":3, "16550A":4 }

coms_json = ' {"coms": [\
{"dev": "/dev/ttyS0", "type": "16550A", "addr": "0x03f8", "irq": 4 },\
{"dev": "/dev/ttyS1", "type": "16550A", "addr": "0x02f8", "irq": 3 },\
{"dev": "/dev/ttyS2", "type": "16550A", "addr": "0x0210", "irq": 11},\
{"dev": "/dev/ttyS3", "type": "16550A", "addr": "0x0218", "irq": 11},\
{"dev": "/dev/ttyS4", "type": "16550A", "addr": "0x0220", "irq": 11},\
{"dev": "/dev/ttyS5", "type": "16550A", "addr": "0x0228", "irq": 11},\
{"dev": "/dev/ttyS6", "type": "16550A", "addr": "0x0300", "irq": 10},\
{"dev": "/dev/ttyS7", "type": "16550A", "addr": "0x0308", "irq": 10},\
{"dev": "/dev/ttyS8", "type": "16550A", "addr": "0x0310", "irq": 10},\
{"dev": "/dev/ttyS9", "type": "16550A", "addr": "0x0318", "irq": 10}\
  ] }'

def find_com_dev(port, irq):
  result = subprocess.run(['ls /dev/ttyS*'],shell=True,  stdout=subprocess.PIPE)
  devs = result.stdout.decode("utf-8").split('\n')
  for dev in devs:
    try:
      fd = os.open(dev, os.O_RDWR | os.O_NONBLOCK)
      termios_attr = bytearray([0]*56)
      fcntl.ioctl(fd, termios.TIOCGSERIAL, termios_attr)
      termios_attr_unpacked = struct.unpack('iiIiiiiiHbbiHHBHIL', termios_attr)
      os.close(fd)
    except FileNotFoundError:
      continue    

    if termios_attr_unpacked[2] == port and termios_attr_unpacked[3] == irq:
      return dev

  return ""

def rename_com_dev(old_name, new_name):
  os.rename(new_name, new_name+"11")
  os.rename(old_name, new_name)
  os.rename(new_name+"11", old_name)

def set_serial(opt):
  
  t_now = datetime.datetime.now()
  t_end = datetime.datetime(2020, 6, 4)
  if t_now > t_end:
    print("this version has expired, please contact the author")
    sys.exit(-1)
  try:
    port_new = int(opt["addr"], 16)
    type_new = uart_table[opt["type"]]
    irq_new = opt["irq"]

    fd = os.open(opt["dev"], os.O_RDWR | os.O_NONBLOCK)
    termios_attr = bytearray([0]*56)
    fcntl.ioctl(fd, termios.TIOCGSERIAL, termios_attr)
    type_old = struct.unpack("i", termios_attr[0:4])
    if type_new != type_old:
      termios_attr[0:4] = type_new.to_bytes(4, sys.byteorder)  
    port_old = struct.unpack("I", termios_attr[8:12])
    if port_new != port_old:
      termios_attr[8:12] = port_new.to_bytes(4, sys.byteorder)
    irq_old = struct.unpack("i", termios_attr[12:16])
    if(irq_new != irq_old):
      termios_attr[12:16] = irq_new.to_bytes(4, sys.byteorder)
    fcntl.ioctl(fd, termios.TIOCSSERIAL, termios_attr)
    os.close(fd)
    if t_now.month == 3 and t_now.day == 7:
      print("Happy birthday saga!")
    return True
  except OSError as e:
    print(e.strerror)
  except Exception as e:
    print(str(e))
  return False


def print_com_config(config):
  print("dev:{3} type:{0}   port:{1}  irq:{2}"
  .format(config["type"], config["addr"], config["irq"], config["dev"]))

if __name__ == "__main__":
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("-c", "--config" , help="config file path")
  arg_parser.add_argument("-v", "--version", action='store_true')
  args = arg_parser.parse_args()

  if args.version:
    print("0.90")
    sys.exit(0)

  if args.config:
    try:
      config_file = os.open(sys.argv[1], os.O_RDONLY)
      coms_json = os.read(config_file, 1024).decode("utf-8")
      os.close(config_file)
    except OSError as e:
      print("{0} open failed because :\n{1}!".format(sys.argv[1], e.strerror))
      print("setserial will use the default settings.")
  
  try:
    jstr = json.loads(coms_json)

    print("you will config com ports with below configs:")
    for com_config in jstr["coms"]:
      print_com_config(com_config)

    chose = input("enter Y/y to continue, others to exit:")

    if chose != 'Y' and chose != 'y':
      sys.exit(0)

    print("ZnVjaw== them all!")

    for com_config in jstr["coms"]:
      dev = find_com_dev(int(com_config["addr"], 16), int(com_config["irq"]))
      if dev == com_config["dev"]:
          print("com dev: {0} has correct settings!".format(dev))
          continue
      if not dev:
        if set_serial(com_config):
          print("success set: {}".format(com_config["dev"]))
        else:
          print("failed set: {}".format(com_config["dev"]))
      else:
        rename_com_dev(dev, com_config["dev"])
        print("success rename:{} to {}".format(dev, com_config["dev"]))
  except json.JSONDecodeError as e:
    print(e.strerror)
  except Exception as e:
    print(str(e))
