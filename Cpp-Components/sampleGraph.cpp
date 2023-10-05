#include <iostream>
#include <unordered_map>

#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

// Sample knowledgeGraph
std::unordered_map<std::string, std::vector<std::string>> knowledgeGraph = {
    {"cat", {"animal", "pet"}},   {"dog", {"animal", "pet"}},
    {"animal", {"living_being"}}, {"pet", {"domesticated_animal"}},
    {"living_being", {}},         {"domesticated_animal", {}}};

std::vector<double> generateEmbedding(const std::string &word) {
  std::vector<double> embedding;

  if (knowledgeGraph.find(word) != knowledgeGraph.end()) {
    for (const std::string &related : knowledgeGraph[word]) {
      embedding.push_back(1.0);
    }
  } else {
    embedding.push_back(0.0);
  }

  return embedding;
}

int main() {
  std::string inputWord = "cat";
  std::vector<double> embedding = generateEmbedding(inputWord);

  std::cout << "Embedding for '" << inputWord << "': ";
  for (double value : embedding) {
    std::cout << value << " ";
  }
  std::cout << std::endl;

  return 0;
}
