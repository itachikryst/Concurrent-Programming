import os
import select
import struct


def encode_msg_size(__size):
		return struct.pack("<I", __size)


def decode_msg_size(size_bytes):
		return struct.unpack("<I", size_bytes)[0]


def create_msg(content):
		__size = len(content)
		return encode_msg_size(__size) + content


def get_message(fifo):
		msg_size_bytes = os.read(fifo, 4)
		msg_size = decode_msg_size(msg_size_bytes)
		msg_content = os.read(fifo, msg_size).decode("utf8")
		return msg_content


serverFifoFileName = "/home/runner/serwerfifo"
serverFifo = os.open(serverFifoFileName, os.O_WRONLY)
clientFifoFileName = "klientfifo"
try:
	os.mkfifo(clientFifoFileName)
except:
	os.remove(clientFifoFileName)
	os.mkfifo(clientFifoFileName)
clientFifo = os.open(clientFifoFileName, os.O_RDONLY | os.O_NONBLOCK)

id = input("Enter an id: ")
id = f"{id}".encode("utf8")
filePath = f"{os.path.abspath(__file__)[:-9]+clientFifoFileName}".encode("utf8")
msg = create_msg(id+filePath)
os.write(serverFifo, msg)

poll = select.poll()
poll.register(clientFifo, select.POLLIN)
if (clientFifo, select.POLLIN) in poll.poll(2147483647):
		print(get_message(clientFifo))

poll.unregister(clientFifo)
os.close(serverFifo)
os.close(clientFifo)
os.remove(clientFifoFileName)