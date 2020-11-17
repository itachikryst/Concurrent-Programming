#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>
#include <filesystem>

std::string getUserInput();
void saveStringToFile(std::string fileName, std::string content);
std::string saveFileToString(std::string fileName);
int main(int argc, char* argv[]) {
	if (argc < 2) {
		std::cout << "You didn't enter the server name!";
		return 0;
	}
	std::string serverName = argv[1];
	std::string clientRequestFile = "clientRequest" + serverName + ".txt";
	std::string clientRequestLockFile = "clientRequest" + serverName + ".lock";
	std::string clientResponseFile = "clientResponse" + serverName + ".txt";
	std::string clientResponseLockFile = "clientResponse" + serverName + ".lock";
	std::string serverResponseFile = "serverResponse" + serverName + ".txt";

	while (true) {
		std::ifstream tempFile;
		tempFile.open(clientRequestLockFile);
		std::ifstream tempFile2;
		tempFile2.open(clientResponseLockFile);
		if (tempFile.good() && tempFile2.good())
		{
			std::string clientName = saveFileToString(clientRequestFile);
			std::string clientMessage = saveFileToString(clientResponseFile);
			std::cout << clientName << ": " << clientMessage;
			std::string serverMessage;
			std::cout << "\nWhat is your response?: ";
			serverMessage = getUserInput();
			saveStringToFile(serverResponseFile, serverMessage);
			tempFile.close();
			tempFile2.close();
			remove(clientRequestFile.c_str());
			remove(clientRequestLockFile.c_str());
			remove(clientResponseFile.c_str());
			remove(clientResponseLockFile.c_str());
		}
		
	}
	return 0;
}
std::string getUserInput() {
	std::string temp = "";
	std::string line;
	while (std::getline(std::cin, line))
	{
		if (line == "/eof") break;
		temp += line;
	}
	return temp;
}
void saveStringToFile(std::string fileName, std::string content) {
	std::ofstream tempFile;
	tempFile.open(fileName);
	tempFile << std::noskipws << content;
	tempFile.close();
}
std::string saveFileToString(std::string fileName) {
	std::string content = "";
	char character;
	std::ifstream tempFile(fileName);
	if (tempFile.is_open()) {
		while (tempFile.get(character))
		{
			content += character;
		}
		tempFile.close();
	}
	return content;
}