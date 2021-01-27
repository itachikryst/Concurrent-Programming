import sysv_ipc


inputKey = 987654321
outputKey = 123456789
inputQueue = sysv_ipc.MessageQueue(inputKey, sysv_ipc.IPC_CREAT)
outputQueue = sysv_ipc.MessageQueue(outputKey, sysv_ipc.IPC_CREAT)
translationDictionary	= {
		"dog" : "pies",
		"cat" : "kot",
		"cow" : "krowa",
		"crow" : "wrona",
		"wolf" : "wilk",
		"squirell" : "wiewiórka",
		"mousedeer" : "myszojeleń",
		"raven" : "kruk",
		"stork" : "niemaszsianazadzwondobociana"
}


def findInDict(clientRequest):
		for eng, pol in translationDictionary.items():
				if eng == clientRequest:
						return pol
		return "No word such as " + eng + " in the dictionary."


messageList = []
while(True):
		if len(messageList) != 0:
			for _message in messageList:
				outputQueue.send(_message[1].decode().split(":")[0].encode())
		messageRaw, _type = inputQueue.receive()
		messageDecoded = messageRaw.decode()
		englishWord, pid = messageDecoded.split(":")
		messageList.append([pid, messageRaw, _type])
		polishWord = findInDict(englishWord)
		polishWordEncoded = polishWord.encode()
		outputQueue.send(polishWordEncoded)
		for _message in messageList:
			if _message[0] == pid:
				messageList.remove(_message)