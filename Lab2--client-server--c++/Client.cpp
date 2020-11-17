#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>
#include <filesystem>

std::string getUserInput();
void checkLockFile(std::string fileName);
void saveStringToFile(std::string fileName, std::string content);
std::string saveFileToString(std::string fileName);
int main(int argc, char* argv[]) {
	if(argc < 2){
		std::cout << "You didn't enter the server name!";
		return 0;
	}
	std::string serverName = argv[1];
	std::string clientRequestFile = "clientRequest"+serverName+".txt";
	std::string clientRequestLockFile = "clientRequest" + serverName + ".lock";
	std::string clientResponseFile = "clientResponse" + serverName + ".txt";
	std::string clientResponseLockFile = "clientResponse" + serverName + ".lock";
	std::string serverResponseFile = "serverResponse" + serverName + ".txt";
	std::cout << "Enter your name: ";
	std::string clientName;
	clientName = getUserInput();
	std::cout << "Enter your message: ";
	std::string clientResponse;
	clientResponse = getUserInput();
	checkLockFile(clientRequestLockFile);
	saveStringToFile(clientRequestFile, clientName);
	checkLockFile(clientResponseLockFile);
	saveStringToFile(clientResponseFile, clientResponse);
	std::ifstream tempFile;
	tempFile.open(serverResponseFile);
	while (!tempFile.good())
	{
		tempFile.close();
		std::cout << "No server response, please wait" << std::endl;
		std::this_thread::sleep_for(std::chrono::seconds(1));
		tempFile.open(serverResponseFile);
	}
	tempFile.close();
	std::string serverResponse = saveFileToString(serverResponseFile);
	std::cout << "Server response: " << serverResponse << std::endl;
	remove(serverResponseFile.c_str());
	std::this_thread::sleep_for(std::chrono::seconds(5));
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
void checkLockFile(std::string fileName) {
	std::ifstream tempFile;
	tempFile.open(fileName);
	while (tempFile.good())
	{
		tempFile.close();
		std::cout << "Server is busy now, wait 5 seconds for the next chance to join" << std::endl;
		std::this_thread::sleep_for(std::chrono::seconds(5));
		tempFile.open(fileName);
	}
	if (!tempFile.is_open()) {
		tempFile.close();
		std::ofstream tempFile;
		tempFile.open(fileName);
		tempFile.close();
	}
}