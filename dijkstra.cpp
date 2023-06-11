#include <iostream>
#include <fstream>
#include <vector>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

struct Edge {
    unsigned short int neighbor;
    unsigned short int weight;
};

class Graph {
private:
    std::vector<std::vector<Edge>> graph;
    std::vector<unsigned short int> hu;

    bool readGraphFromFile(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Wrong file" << std::endl;
            return false;
        }

        json graphJson;
        file >> graphJson;

        for (const auto& vertexJson : graphJson["graph"]) {
            std::vector<Edge> vertexEdges;

            for (const auto& edgeJson : vertexJson) {
                unsigned short int neighbor = edgeJson[0];
                unsigned short int weight = edgeJson[1];

                Edge edge{neighbor, weight};
                vertexEdges.push_back(edge);
            }

            graph.push_back(vertexEdges);
        }

        hu = graphJson["hu"].get<std::vector<unsigned short int>>();

        return true;
    }

public:
    Graph(const std::string& filename) {
        readGraphFromFile(filename);
    }

    bool is_hu(unsigned short int vertex) const {
        for (unsigned short int v : hu) {
            if (v == vertex) {
                return true;
            }
        }
        return false;
    }

    void printGraph() const {
        std::cout << "Graph:" << std::endl;
        for (const auto& vertexEdges : graph) {
            for (const auto& edge : vertexEdges) {
                std::cout << "(" << edge.neighbor << ", " << edge.weight << ") ";
            }
            std::cout << std::endl;
        }

        std::cout << "hu: [";
        for (size_t i = 0; i < hu.size(); ++i) {
            std::cout << hu[i];
            if (i != hu.size() - 1) {
                std::cout << ", ";
            }
        }
        std::cout << "]" << std::endl;
    }
};

int main() {
    Graph graph("./test/001.json");

    graph.printGraph();

    //std::cout << (graph.is_hu(9) ? "9 benne van" : "9 nincs benne") << std::endl;
    //std::cout << (graph.is_hu(4) ? "4 benne van" : "4 nincs benne") << std::endl;

    return 0;
}
