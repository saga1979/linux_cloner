import termios os fcntl json  struct sys


uart_table = { "8250": 1, "16450":2, "16550":3, "16550A":4 }

coms_json = ' {"coms": [\
{"dev": "/dev/ttyS0", "UART": "16550A", "Port": "0x03f8", "IRQ": 4 },\
{"dev": "/dev/ttyS1", "UART": "16550A", "Port": "0x02f8", "IRQ": 3 },\
{"dev": "/dev/ttyS2", "UART": "16550A", "Port": "0x03e8", "IRQ": 7},\
{"dev": "/dev/ttyS3", "UART": "16550A", "Port": "0x02e8", "IRQ": 7},\
{"dev": "/dev/ttyS4", "UART": "16550A", "Port": "0x02f0", "IRQ": 7},\
{"dev": "/dev/ttyS5", "UART": "16550A", "Port": "0x02e0", "IRQ": 7},\
{"dev": "/dev/ttyS6", "UART": "16550A", "Port": "0x0240", "IRQ": 6},\
{"dev": "/dev/ttyS7", "UART": "16550A", "Port": "0x0248", "IRQ": 6},\
{"dev": "/dev/ttyS8", "UART": "16550A", "Port": "0x0250", "IRQ": 11},\
{"dev": "/dev/ttyS9", "UART": "16550A", "Port": "0x0258", "IRQ": 11}\
  ] }'


jstr = json.loads(coms_json)



def set_serial(opt):
  print("set serial:" + opt["dev"])
  port_new = int(opt["Port"], 16)
  type_new = uart_table[opt["UART"]]
  irq_new = opt["IRQ"]

  print("port:0x{0:X}".format(port_new))
  fd = os.open(opt["dev"], os.O_RDWR | os.O_NONBLOCK)

  termios_attr = bytearray([0]*56)
  fcntl.ioctl(fd, termios.TIOCGSERIAL, termios_attr)
  print(termios_attr)
  termios_old_unpacked = struct.unpack('iiIiiiiiHbbiHHBHIL', termios_attr)
  print(termios_old_unpacked)
  termios_old_list = list(termios_old_unpacked)

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

# for com in jstr["coms"]:
#   set_serial(com)

set_serial(jstr["coms"][0])