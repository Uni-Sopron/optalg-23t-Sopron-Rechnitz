#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <limits>
#include <set>

#include <nlohmann/json.hpp>

using json = nlohmann::json;

struct Edge {
    unsigned short int neighbor;
    unsigned short int weight;
};

class Graph {
private:
    std::vector<std::vector<Edge>> graph;
    std::set<unsigned short int> hu;
    std::unordered_map<unsigned short int, unsigned short int> distances;

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

        hu = std::set<unsigned short int>(graphJson["hu"].begin(), graphJson["hu"].end());

        return true;
    }

    bool is_hu(unsigned short int vertex) const {
        return hu.find(vertex) != hu.end();
    }

    void computeDistances(unsigned short int startVertex) {
        distances.clear();

        for (unsigned short int vertex = 0; vertex < graph.size(); ++vertex) {
            distances[vertex] = std::numeric_limits<unsigned short int>::max();
        }

        distances[startVertex] = 0;

        std::set<unsigned short int> unvisited;
        for (unsigned short int vertex = 0; vertex < graph.size(); ++vertex) {
            unvisited.insert(vertex);
        }

        while (!unvisited.empty()) {
            unsigned short int minDistanceVertex = *unvisited.begin();
            for (unsigned short int vertex : unvisited) {
                if (distances[vertex] < distances[minDistanceVertex]) {
                    minDistanceVertex = vertex;
                }
            }

            unvisited.erase(minDistanceVertex);

            for (const auto& edge : graph[minDistanceVertex]) {
                unsigned short int neighbor = edge.neighbor;
                unsigned short int weight = edge.weight;

                if (is_hu(minDistanceVertex) || is_hu(neighbor)) {
                    unsigned short int newDistance = distances[minDistanceVertex] + weight;
                    if (newDistance < distances[neighbor]) {
                        distances[neighbor] = newDistance;
                    }
                }
            }
        }
    }

public:
    Graph(const std::string& filename) {
        readGraphFromFile(filename);
    }

    void printGraph() const {
        std::cout << "Graph:" << std::endl;
        for (const auto& vertexEdges : graph) {
            for (const auto& edge : vertexEdges) {
                std::cout << "(" << edge.neighbor << ", " << edge.weight << ") ";
            }
            std::cout << std::endl;
        }

        std::cout << "hu: ";
        for (const auto& v : hu) {
            std::cout << v << " ";
        }
        std::cout << std::endl;
    }

    void shortest_path(unsigned short int from, unsigned short int to) {
        if (distances.empty()) {
            computeDistances(from);
        }

        std::cout << std::to_string(from) << " -> " << std::to_string(to) << ": ";
        if (distances.at(to) == std::numeric_limits<unsigned short int>::max()) {
            std::cout << "No path exists." << std::endl;
        } else {
            std::cout << distances.at(to) << std::endl;
        }
    }
};

int main() {
    Graph graph("./test/001.json");

    graph.printGraph();

    unsigned short int vertex1 = 10;
    unsigned short int vertex2 = 1;

    graph.shortest_path(0, 0);
    graph.shortest_path(0, 1);
    graph.shortest_path(0, 2);
    graph.shortest_path(0, 3);

    return 0;
}
