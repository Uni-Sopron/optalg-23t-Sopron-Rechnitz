#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <set>
#include <algorithm>

#include <nlohmann/json.hpp>

using json = nlohmann::json;

struct Edge
{
    unsigned short int neighbor;
    unsigned short int weight;
};

class Graph
{
private:
    std::vector<std::vector<Edge>> graph;
    std::set<unsigned short int> hu;
    std::unordered_map<unsigned short int, unsigned short int> distances;
    std::unordered_map<unsigned short int, unsigned short int> parent;
    std::unordered_map<unsigned short int, unsigned short int> switchCount;

    bool isHu(unsigned short int vertex) const
    {
        return hu.find(vertex) != hu.end();
    }

    void addEdges(const json &vertexJson, std::vector<Edge> &vertexEdges)
    {
        for (const auto &edgeJson : vertexJson)
        {
            vertexEdges.push_back(Edge{edgeJson[0], edgeJson[1]});
        }
    }

    void redadAdjacencyList(const json &graphJson)
    {
        for (const auto &vertexJson : graphJson["graph"])
        {
            std::vector<Edge> vertexEdges;
            addEdges(vertexJson, vertexEdges);
            graph.push_back(vertexEdges);
        }
    }

    void readHu(const json &graphJson)
    {
        hu.insert(graphJson["hu"].begin(), graphJson["hu"].end());
    }

    void initializeDistances()
    {
        for (size_t i = 0; i < graph.size(); ++i)
        {
            distances[i] = std::numeric_limits<unsigned short int>::max();
        }
    }

    bool readGraphFromFile(const std::string &filename)
    {
        std::ifstream file(filename);
        if (!file.is_open())
        {
            std::cerr << "Could not open file." << std::endl;
            return false;
        }

        json graphJson;
        file >> graphJson;

        redadAdjacencyList(graphJson);
        readHu(graphJson);
        initializeDistances();

        return true;
    }

    unsigned short int getMinVertex(const std::vector<bool> &processed, unsigned short int invalid_vertex)
    {
        unsigned short int vertex = invalid_vertex;
        for (unsigned short int j = 0; j < graph.size(); ++j)
        {
            if (!processed[j] && (vertex == invalid_vertex || distances[j] < distances[vertex]))
            {
                vertex = j;
            }
        }
        return vertex;
    }

    void processVertex(unsigned short int vertex, const std::vector<bool> &processed)
    {
        for (const auto &edge : graph[vertex])
        {
            unsigned short int nextSwitchCount = switchCount[vertex] + (isHu(vertex) != isHu(edge.neighbor) ? 1 : 0);
            if (nextSwitchCount <= 1 && distances[vertex] + edge.weight < distances[edge.neighbor])
            {
                distances[edge.neighbor] = distances[vertex] + edge.weight;
                parent[edge.neighbor] = vertex;
                switchCount[edge.neighbor] = nextSwitchCount;
            }
        }
    }

    void computeDistances(unsigned short int startVertex)
    {
        std::vector<bool> processed(graph.size(), false);
        distances[startVertex] = 0;
        switchCount[startVertex] = 0;
        unsigned short int invalid_vertex = std::numeric_limits<unsigned short int>::max();

        for (size_t i = 0; i < graph.size(); ++i)
        {
            unsigned short int vertex = getMinVertex(processed, invalid_vertex);

            if (distances[vertex] == std::numeric_limits<unsigned short int>::max())
            {
                break;
            }

            processed[vertex] = true;
            processVertex(vertex, processed);
        }
    }

    void printPath(unsigned short int from, unsigned short int to)
    {
        if (distances[to] == std::numeric_limits<unsigned short int>::max())
        {
            std::cout << "No path from " << from << " to " << to << std::endl;
            return;
        }

        std::vector<unsigned short int> path;
        for (unsigned short int v = to; v != from; v = parent[v])
        {
            path.push_back(v);
        }
        path.push_back(from);

        std::reverse(path.begin(), path.end());

        std::cout << "Path from " << from << " to " << to << " with total distance: " << distances[to] << "\n";
        for (const auto &vertex : path)
        {
            std::cout << vertex << " ";
        }
        std::cout << std::endl;
    }

public:
    Graph(const std::string &filename)
    {
        readGraphFromFile(filename);
    }

    void printGraph()
    {
        for (size_t i = 0; i < graph.size(); i++)
        {
            std::cout << (isHu(i) ? "hu - " : "at - ") << i << ": ";
            for (const auto &edge : graph[i])
            {
                std::cout << "{" << edge.neighbor << ", " << edge.weight << "} ";
            }
            std::cout << std::endl;
        }
        std::cout << std::endl;
    }

    void getShortestPath(unsigned short int from, unsigned short int to)
    {
        computeDistances(from);
        printPath(from, to);
    }
};

int main()
{
    Graph graph("./test/001.json");

    graph.printGraph();

    graph.getShortestPath(3, 6);
    graph.getShortestPath(0, 1);
    graph.getShortestPath(0, 2);
    graph.getShortestPath(0, 3);
    graph.getShortestPath(0, 4);
    graph.getShortestPath(0, 5);
    graph.getShortestPath(0, 6);
    graph.getShortestPath(0, 7);
    graph.getShortestPath(0, 8);
    graph.getShortestPath(0, 9);

    return 0;
}
