#include <algorithm>
#include <cctype>
#include <fstream>
#include <iostream>
#include <locale>
#include <sstream>
#include <string>
#include <vector>

// Function to preprocess text
std::vector<std::string> preprocessText(const std::string &text) {
  std::vector<std::string> tokens;
  std::istringstream iss(text);
  std::string token;

  while (iss >> token) {
    std::transform(token.begin(), token.end(), token.begin(), ::tolower);
    token.erase(std::remove_if(token.begin(), token.end(), ::ispunct),
                token.end());
    tokens.push_back(token);
  }

  return tokens;
}

int main() {
  std::ifstream inputFile("corpus.txt");
  std::string corpusText;

  if (inputFile.is_open()) {
    std::stringstream buffer;
    buffer << inputFile.rdbuf();
    corpusText = buffer.str();
  } else {
    std::cerr << "Error: Could not open the input file." << std::endl;
    return 1;
  }

  std::vector<std::string> tokens = preprocessText(corpusText);

  inputFile.close();
  return 0;
}
