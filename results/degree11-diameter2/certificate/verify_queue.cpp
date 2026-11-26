#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 3) return 1;
    constexpr int n = 108;
    std::array<std::vector<int>, n> neighbors;
    std::ifstream edges(argv[1]);
    if (!edges) return 2;
    int edge_count = 0;
    for (std::string line; std::getline(edges, line);) {
        std::istringstream input(line);
        int u, v;
        std::string extra;
        if (!(input >> u >> v) || (input >> extra)) return 3;
        if (u < 0 || u >= n || v < 0 || v >= n || u == v) return 4;
        neighbors[u].push_back(v);
        neighbors[v].push_back(u);
        ++edge_count;
    }
    for (auto& row : neighbors) {
        std::sort(row.begin(), row.end());
        if (row.size() != 11 || std::adjacent_find(row.begin(), row.end()) != row.end()) return 5;
    }
    std::array<int, n> histogram{};
    std::ofstream matrix(argv[2], std::ios::binary);
    if (!matrix) return 6;
    for (int source = 0; source < n; ++source) {
        std::array<std::uint8_t, n> distance;
        distance.fill(255);
        std::queue<int> pending;
        pending.push(source);
        distance[source] = 0;
        while (!pending.empty()) {
            int u = pending.front();
            pending.pop();
            for (int v : neighbors[u]) {
                if (distance[v] != 255) continue;
                distance[v] = distance[u] + 1;
                pending.push(v);
            }
        }
        for (int v = 0; v < n; ++v) {
            if (distance[v] == 255) return 7;
            if (source < v) ++histogram[distance[v]];
        }
        matrix.write(reinterpret_cast<const char*>(distance.data()), n);
    }
    matrix.close();
    if (!matrix || edge_count != 594 || histogram[1] != 594 || histogram[2] != 5184) return 8;
    std::cout << "vertices=108 degree=11 edges=594 diameter=2 unordered_distance_1="
              << histogram[1] << " unordered_distance_2=" << histogram[2] << '\n';
}
