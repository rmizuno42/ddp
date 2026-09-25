// Exact edge-list verification using bit-parallel breadth-first search.
// Every source is checked. No construction, symmetry, or saved certificate is used.
// Usage: verify_edges FILE N DEGREE DIAMETER HAS_HEADER THREADS SOURCE_BATCH
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <utility>
#include <vector>

int main(int argc, char** argv) {
    try {
        if (argc != 8) throw std::runtime_error(
            "usage: verify_edges FILE N DEGREE DIAMETER HAS_HEADER THREADS SOURCE_BATCH");
        const int n = std::stoi(argv[2]), degree = std::stoi(argv[3]);
        const int diameter = std::stoi(argv[4]), header = std::stoi(argv[5]);
        const int workers = std::stoi(argv[6]), batch_size = std::stoi(argv[7]);
        if (n <= 0 || degree < 0 || diameter < 1 || workers < 1 || workers > 64 ||
            batch_size < 1 || (header != 0 && header != 1))
            throw std::runtime_error("invalid parameters");
        const auto started = std::chrono::steady_clock::now();
        std::ifstream file(argv[1]);
        if (!file) throw std::runtime_error("cannot open edge list");
        std::string line, extra;
        std::uint64_t declared_edges = 0, edges = 0;
        if (header) {
            if (!std::getline(file, line)) throw std::runtime_error("missing header");
            std::istringstream row(line);
            int declared_n;
            if (!(row >> declared_n >> declared_edges) || (row >> extra) || declared_n != n)
                throw std::runtime_error("invalid header or vertex count");
        }
        std::vector<std::vector<int>> adjacency(n);
        while (std::getline(file, line)) {
            std::istringstream row(line);
            int u, v;
            if (!(row >> u >> v) || (row >> extra) || u < 0 || v < 0 ||
                u >= n || v >= n || u == v)
                throw std::runtime_error("invalid edge or self-loop at edge " + std::to_string(edges + 1));
            adjacency[u].push_back(v);
            adjacency[v].push_back(u);
            ++edges;
        }
        if (!file.eof()) throw std::runtime_error("error reading edge list");
        if (header && edges != declared_edges) throw std::runtime_error("header edge count mismatch");
        std::map<int, int> degrees;
        for (auto& row : adjacency) {
            std::sort(row.begin(), row.end());
            if (std::adjacent_find(row.begin(), row.end()) != row.end())
                throw std::runtime_error("duplicate undirected edge");
            ++degrees[static_cast<int>(row.size())];
        }
        if (degrees.rbegin()->first != degree) throw std::runtime_error("maximum degree differs from claim");

        // At radius k, current[v] records exactly the sources in this batch
        // at distance <= k from v. One synchronous union with every neighbor
        // computes radius k+1. Batching changes only memory use, not coverage.
        std::vector<std::uint64_t> histogram(diameter + 1, 0);
        histogram[0] = n;
        std::uint64_t total_reached = 0;
        std::pair<int, int> witness{-1, -1};
        for (int base = 0; base < n; base += batch_size) {
            const int batch = std::min(batch_size, n - base);
            const std::size_t words = (static_cast<std::size_t>(batch) + 63) / 64;
            std::vector<std::uint64_t> current(static_cast<std::size_t>(n) * words, 0);
            std::vector<std::uint64_t> next(current.size(), 0);
            for (int source = 0; source < batch; ++source)
                current[static_cast<std::size_t>(base + source) * words + source / 64] =
                    std::uint64_t{1} << (source % 64);
            std::uint64_t previous = batch;
            for (int step = 1; step <= diameter; ++step) {
                std::vector<std::uint64_t> counts(workers, 0);
                std::vector<std::pair<int, int>> witnesses(workers, {-1, -1});
                std::vector<std::thread> threads;
                for (int worker = 0; worker < workers; ++worker) {
                    threads.emplace_back([&, worker]() {
                        const int begin = static_cast<std::int64_t>(n) * worker / workers;
                        const int end = static_cast<std::int64_t>(n) * (worker + 1) / workers;
                        std::uint64_t count = 0;
                        for (int v = begin; v < end; ++v) {
                            auto* out = next.data() + static_cast<std::size_t>(v) * words;
                            const auto* old = current.data() + static_cast<std::size_t>(v) * words;
                            std::copy_n(old, words, out);
                            for (int u : adjacency[v]) {
                                const auto* in = current.data() + static_cast<std::size_t>(u) * words;
                                for (std::size_t word = 0; word < words; ++word) out[word] |= in[word];
                            }
                            for (std::size_t word = 0; word < words; ++word) {
                                count += __builtin_popcountll(out[word]);
                                if (step == diameter && witnesses[worker].first < 0) {
                                    const auto added = out[word] & ~old[word];
                                    if (added) witnesses[worker] = {
                                        base + static_cast<int>(word * 64) + __builtin_ctzll(added), v};
                                }
                            }
                        }
                        counts[worker] = count;
                    });
                }
                for (auto& thread : threads) thread.join();
                std::uint64_t reached = 0;
                for (int worker = 0; worker < workers; ++worker) {
                    reached += counts[worker];
                    if (witness.first < 0 && witnesses[worker].first >= 0) witness = witnesses[worker];
                }
                if (reached < previous) throw std::runtime_error("non-monotone reachability");
                histogram[step] += reached - previous;
                previous = reached;
                current.swap(next);
            }
            total_reached += previous;
            std::cerr << "sources checked: " << base + batch << '/' << n << '\n';
        }
        const auto pairs = static_cast<std::uint64_t>(n) * n;
        const bool connected_within_bound = total_reached == pairs;
        int measured_diameter = 0;
        for (int d = 1; d <= diameter; ++d) if (histogram[d]) measured_diameter = d;
        const bool passed = connected_within_bound && measured_diameter == diameter;
        const double seconds = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started).count();
        std::cout << "{\n  \"status\": \"" << (passed ? "PASS" : "FAIL")
                  << "\",\n  \"method\": \"exact bit-parallel BFS; all sources in batches\",\n"
                  << "  \"vertices\": " << n << ",\n  \"edges\": " << edges
                  << ",\n  \"maximum_degree\": " << degrees.rbegin()->first
                  << ",\n  \"degree_histogram\": {";
        bool first = true;
        for (const auto& item : degrees) {
            if (!first) std::cout << ", ";
            first = false;
            std::cout << '"' << item.first << "\": " << item.second;
        }
        std::cout << "},\n  \"simple\": true,\n  \"connected\": "
                  << (connected_within_bound ? "true" : "null")
                  << ",\n  \"diameter\": "
                  << (connected_within_bound ? std::to_string(measured_diameter) : "null")
                  << ",\n  \"all_sources_checked\": " << n
                  << ",\n  \"ordered_pairs_checked\": " << pairs
                  << ",\n  \"unreachable_within_claimed_diameter\": " << pairs - total_reached
                  << ",\n  \"distance_histogram_ordered_pairs\": [";
        for (int d = 0; d <= diameter; ++d) {
            if (d) std::cout << ", ";
            std::cout << histogram[d];
        }
        std::cout << "],\n  \"claimed_diameter_witness\": [" << witness.first << ", " << witness.second
                  << "],\n  \"threads\": " << workers << ",\n  \"source_batch_size\": " << batch_size
                  << ",\n  \"elapsed_seconds\": " << seconds << "\n}\n";
        return passed ? 0 : 1;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
