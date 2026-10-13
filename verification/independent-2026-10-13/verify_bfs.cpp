// Independent ordinary all-source BFS. Input: an undirected edge list only.
// No construction data, claimed degree/diameter, symmetry, or prior report.
// Usage: verify_bfs EDGE_FILE THREADS
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <utility>
#include <vector>

using Count = std::uint64_t;

struct Tally {
    std::vector<Count> distances;
    std::map<int, Count> eccentricities;
    Count sources = 0, unreachable = 0;
    int largest_distance = -1;
    std::pair<int, int> witness{-1, -1};
};

static void require(bool value, const char* message) {
    if (!value) throw std::runtime_error(message);
}

int main(int argc, char** argv) {
    try {
        require(argc == 3, "Usage: verify_bfs EDGE_FILE THREADS");
        const auto start = std::chrono::steady_clock::now();
        const int workers = std::stoi(argv[2]);
        require(workers >= 1 && workers <= 64, "Invalid thread count");
        std::ifstream input(argv[1]);
        require(bool(input), "Cannot open edge list");
        std::string line, extra;
        require(bool(std::getline(input, line)), "Missing header");
        std::istringstream header(line);
        long long declared_n = 0, declared_m = 0;
        require(bool(header >> declared_n >> declared_m) && !(header >> extra),
                "Header must contain exactly n and m");
        require(declared_n > 0 && declared_n <= std::numeric_limits<int>::max()
                && declared_m >= 0, "Invalid graph size");
        const int n = static_cast<int>(declared_n);
        std::vector<std::vector<int>> rows(n);
        Count edges = 0;
        while (std::getline(input, line)) {
            std::istringstream record(line);
            long long u = -1, v = -1;
            require(bool(record >> u >> v) && !(record >> extra), "Malformed edge");
            require(u >= 0 && v >= 0 && u < n && v < n, "Vertex label out of range");
            require(u != v, "Self-loop");
            rows[static_cast<int>(u)].push_back(static_cast<int>(v));
            rows[static_cast<int>(v)].push_back(static_cast<int>(u));
            ++edges;
        }
        require(input.eof() && edges == static_cast<Count>(declared_m),
                "Header edge count mismatch or read error");
        std::map<int, Count> degree_counts;
        int distinct_endpoint_labels = 0;
        std::vector<std::size_t> offsets(n + 1, 0);
        std::vector<int> adjacency;
        for (int u = 0; u < n; ++u) {
            auto& row = rows[u];
            std::sort(row.begin(), row.end());
            require(std::adjacent_find(row.begin(), row.end()) == row.end(),
                    "Duplicate undirected edge");
            ++degree_counts[static_cast<int>(row.size())];
            if (!row.empty()) ++distinct_endpoint_labels;
            adjacency.insert(adjacency.end(), row.begin(), row.end());
            offsets[u + 1] = adjacency.size();
        }
        rows.clear();
        rows.shrink_to_fit();

        std::atomic<int> next_source{0}, finished{0};
        std::vector<Tally> tallies(workers);
        std::vector<std::thread> threads;
        for (int worker = 0; worker < workers; ++worker) {
            threads.emplace_back([&, worker] {
                auto& tally = tallies[worker];
                tally.distances.resize(1, 0);
                std::vector<int> distance(n), queue(n);
                for (;;) {
                    const int source = next_source.fetch_add(1);
                    if (source >= n) break;
                    std::fill(distance.begin(), distance.end(), -1);
                    distance[source] = 0;
                    queue[0] = source;
                    int head = 0, tail = 1, farthest = source, eccentricity = 0;
                    ++tally.distances[0];
                    // No depth limit: stop only once all vertices have been
                    // discovered, or the reachable component is exhausted.
                    while (head < tail && tail < n) {
                        const int u = queue[head++];
                        for (auto j = offsets[u]; j < offsets[u + 1]; ++j) {
                            const int v = adjacency[j];
                            if (distance[v] != -1) continue;
                            const int d = distance[u] + 1;
                            distance[v] = d;
                            queue[tail++] = v;
                            if (static_cast<int>(tally.distances.size()) <= d)
                                tally.distances.resize(d + 1, 0);
                            ++tally.distances[d];
                            if (d > eccentricity) { eccentricity = d; farthest = v; }
                        }
                    }
                    ++tally.sources;
                    tally.unreachable += n - tail;
                    if (tail == n) ++tally.eccentricities[eccentricity];
                    const std::pair<int, int> pair{source, farthest};
                    if (eccentricity > tally.largest_distance ||
                        (eccentricity == tally.largest_distance && pair < tally.witness)) {
                        tally.largest_distance = eccentricity;
                        tally.witness = pair;
                    }
                    const int done = finished.fetch_add(1) + 1;
                    if (done % 16000 == 0) std::cerr << "Sources processed: " << done << '\n';
                }
            });
        }
        for (auto& thread : threads) thread.join();
        Tally total;
        for (const auto& tally : tallies) {
            total.sources += tally.sources;
            total.unreachable += tally.unreachable;
            total.distances.resize(std::max(total.distances.size(), tally.distances.size()), 0);
            for (std::size_t d = 0; d < tally.distances.size(); ++d)
                total.distances[d] += tally.distances[d];
            for (auto [d, count] : tally.eccentricities) total.eccentricities[d] += count;
            if (tally.largest_distance > total.largest_distance ||
                (tally.largest_distance == total.largest_distance && tally.witness < total.witness)) {
                total.largest_distance = tally.largest_distance;
                total.witness = tally.witness;
            }
        }
        Count reached = 0;
        for (auto count : total.distances) reached += count;
        require(total.sources == static_cast<Count>(n) &&
                reached + total.unreachable == Count(n) * n, "Incomplete pair accounting");
        std::cout << "{\n  \"vertices\": " << n
                  << ",\n  \"distinct_vertex_labels_in_edges\": " << distinct_endpoint_labels
                  << ",\n  \"edges\": " << edges
                  << ",\n  \"simple\": true,\n  \"undirected\": true"
                  << ",\n  \"minimum_degree\": " << degree_counts.begin()->first
                  << ",\n  \"maximum_degree\": " << degree_counts.rbegin()->first
                  << ",\n  \"degree_histogram\": {";
        bool first = true;
        for (auto [d, count] : degree_counts) {
            if (!first) std::cout << ", ";
            std::cout << '"' << d << "\": " << count; first = false;
        }
        std::cout << "},\n  \"connected\": " << (total.unreachable == 0 ? "true" : "false")
                  << ",\n  \"diameter\": "
                  << (total.unreachable == 0 ? std::to_string(total.largest_distance) : "null")
                  << ",\n  \"all_sources_checked\": " << total.sources
                  << ",\n  \"ordered_pairs_reached\": " << reached
                  << ",\n  \"unreachable_ordered_pairs\": " << total.unreachable
                  << ",\n  \"distance_histogram_ordered_pairs\": [";
        for (std::size_t d = 0; d < total.distances.size(); ++d) {
            if (d) std::cout << ", ";
            std::cout << total.distances[d];
        }
        std::cout << "],\n  \"eccentricity_histogram\": {";
        first = true;
        for (auto [d, count] : total.eccentricities) {
            if (!first) std::cout << ", ";
            std::cout << '"' << d << "\": " << count; first = false;
        }
        std::cout << "},\n  \"largest_finite_distance_witness\": ["
                  << total.witness.first << ", " << total.witness.second
                  << "],\n  \"elapsed_seconds\": "
                  << std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count()
                  << "\n}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
