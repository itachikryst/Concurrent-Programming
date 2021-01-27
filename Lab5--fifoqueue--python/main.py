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


class Person:
		id: int
		surname: str

		def __init__(self, _id: int, _surname: str):
				self.id = _id
				self.surname = _surname


class Database:
		person_list = []


Database.person_list.append(Person(0, "Kowalski-Kowal-Testu"))
Database.person_list.append(Person(1, "Kowalski-Kowal-Test"))
Database.person_list.append(Person(2, "Kowalski-Kowal-Tes"))
Database.person_list.append(Person(3, "Kowalski-Kowal-Te"))
Database.person_list.append(Person(4, "Kowalski-Kowal-T"))
Database.person_list.append(Person(5, "Kowalski-Kowal-"))
Database.person_list.append(Person(6, "Kowalski-Kowal"))
Database.person_list.append(Person(7, "Kowalski-Kowa"))
Database.person_list.append(Person(8, "Kowalski-Kow"))
Database.person_list.append(Person(9, "Kowalski-Ko"))
Database.person_list.append(Person(10, "Kowalski-K"))
Database.person_list.append(Person(11, "Kowalski-"))
Database.person_list.append(Person(12, "Kowalski"))
Database.person_list.append(Person(13, "Kowalsk"))
Database.person_list.append(Person(14, "Kowals"))
Database.person_list.append(Person(15, "Kowal"))
Database.person_list.append(Person(16, "Kowa"))
Database.person_list.append(Person(17, "Kow"))
Database.person_list.append(Person(18, "Ko"))
Database.person_list.append(Person(19, "K"))

serverFifoFileName = "/home/runner/serwerfifo"
try:
	os.mkfifo(serverFifoFileName)
except:
	os.remove(serverFifoFileName)
	os.mkfifo(serverFifoFileName)

try:
		serverFifo = os.open(serverFifoFileName, os.O_RDONLY | os.O_NONBLOCK)
		try:
				poll = select.poll()
				poll.register(serverFifo, select.POLLIN)
				try:
						while True:
								if (serverFifo, select.POLLIN) in poll.poll(100):
										msgFromClient = get_message(serverFifo)
										id, clientFifoFileName = msgFromClient.split("/", 1)
										id = int(id)
										clientFifo = os.open("/"+clientFifoFileName, os.O_WRONLY)
										try:
											content = f"{Database.person_list[id].surname}".encode("utf8")
										except:
											content = f"Nie ma".encode("utf8")
										msgToSend = create_msg(content)
										os.write(clientFifo, msgToSend)
				finally:
						poll.unregister(serverFifo)
		finally:
				os.close(serverFifo)
				os.close(clientFifo)
finally:
		os.remove(serverFifoFileName)
