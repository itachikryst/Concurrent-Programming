import sysv_ipc
import os

inputKey = 987654321
outputKey = 123456789
inputQueue = sysv_ipc.MessageQueue(inputKey)
outputQueue = sysv_ipc.MessageQueue(outputKey)

userInput = input("Enter a word: ")
pid = os.getpid()
message = userInput + ":" + str(pid)
messageEncoded = message.encode()
inputQueue.send(messageEncoded)
serverResponse, _ = outputQueue.receive()
serverResponseDecoded = serverResponse.decode()
print("Server response: ", serverResponseDecoded)