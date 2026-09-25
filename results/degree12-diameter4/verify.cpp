// Check the supplied headerless edge list by ordinary BFS from every vertex.
// Build: c++ -O3 -std=c++17 verify.cpp -o /tmp/ddp-verify-12-4
// Run:   /tmp/ddp-verify-12-4 certificate/graph_12_4_5832.edges
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("usage: verify <headerless-edge-file>");
        constexpr int n = 5832, degree = 12, diameter = 4;
        std::ifstream input(argv[1]);
        if (!input) throw std::runtime_error("cannot open edge file");
        std::vector<std::vector<int>> adjacent(n);
        std::string line;
        std::size_t edges = 0;
        while (std::getline(input, line)) {
            std::istringstream row(line);
            int u, v;
            std::string extra;
            if (!(row >> u >> v) || (row >> extra) || u < 0 || v < 0 ||
                u >= n || v >= n || u == v)
                throw std::runtime_error("invalid edge at line " + std::to_string(edges + 1));
            adjacent[u].push_back(v);
            adjacent[v].push_back(u);
            ++edges;
        }
        if (!input.eof()) throw std::runtime_error("error reading edge file");
        for (auto& row : adjacent) {
            std::sort(row.begin(), row.end());
            if (std::adjacent_find(row.begin(), row.end()) != row.end())
                throw std::runtime_error("duplicate undirected edge");
            if (row.size() != degree) throw std::runtime_error("graph is not 12-regular");
        }
        if (2 * edges != n * degree) throw std::runtime_error("incorrect edge count");
        std::array<std::uint64_t, diameter + 1> histogram{};
        std::vector<int> distance(n), queue(n);
        for (int source = 0; source < n; ++source) {
            std::fill(distance.begin(), distance.end(), -1);
            distance[source] = 0;
            queue[0] = source;
            int head = 0, tail = 1;
            while (head < tail) {
                int u = queue[head++];
                ++histogram[distance[u]];
                if (distance[u] == diameter) continue;
                for (int v : adjacent[u]) {
                    if (distance[v] != -1) continue;
                    distance[v] = distance[u] + 1;
                    queue[tail++] = v;
                }
            }
            if (tail != n) throw std::runtime_error("not all vertices reached within four steps");
        }
        if (histogram[diameter] == 0) throw std::runtime_error("diameter is less than four");
        std::cout << "{\n  \"method\": \"ordinary BFS from every vertex\",\n"
                  << "  \"vertices\": " << n << ",\n  \"edges\": " << edges
                  << ",\n  \"degree\": " << degree << ",\n  \"diameter\": " << diameter
                  << ",\n  \"simple\": true,\n  \"connected\": true,\n"
                  << "  \"all_sources_checked\": " << n << ",\n  \"distance_histogram\": [";
        for (int d = 0; d <= diameter; ++d) {
            if (d) std::cout << ", ";
            std::cout << histogram[d];
        }
        std::cout << "]\n}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
