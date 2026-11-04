// Export the full automorphism-group order and generators using nauty.
// Input format: n m, followed by m undirected edges u v (zero-based vertices).
#include <nauty/nauty.h>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <vector>

std::vector<std::vector<int>> generators;
void automorphism(int, int* p, int*, int, int, int n) {
    generators.emplace_back(p, p+n);
}
int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("Usage: automorphisms INPUT OUTPUT_JSON");
        std::ifstream input(argv[1]);
        std::string line, extra;
        int n, declared;
        if (!std::getline(input, line)) throw std::runtime_error("Missing header");
        std::istringstream header(line);
        if (!(header >> n >> declared) || (header >> extra) || n < 2 || n > 1024 || declared < 0)
            throw std::runtime_error("Invalid header (maximum 1024 vertices)");
        const int m = SETWORDSNEEDED(n);
        nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
        std::vector<graph> graph_data(n*m), canonical(n*m);
        EMPTYGRAPH(graph_data.data(), m, n);
        std::set<std::pair<int,int>> edges;
        while (std::getline(input, line)) {
            int u, v;
            std::istringstream row(line);
            if (!(row >> u >> v) || (row >> extra) || u < 0 || v < 0 || u >= n || v >= n || u == v)
                throw std::runtime_error("Invalid edge");
            if (u > v) std::swap(u, v);
            if (!edges.insert({u,v}).second) throw std::runtime_error("Duplicate edge");
            ADDONEEDGE(graph_data.data(), u, v, m);
        }
        if (static_cast<int>(edges.size()) != declared) throw std::runtime_error("Edge count mismatch");
        std::vector<int> lab(n), ptn(n), orbits(n);
        DEFAULTOPTIONS_GRAPH(options);
        options.userautomproc = automorphism;
        statsblk stats;
        densenauty(graph_data.data(), lab.data(), ptn.data(), orbits.data(), &options,
                   &stats, m, n, canonical.data());
        if (stats.errstatus) throw std::runtime_error("nauty failure");
        std::ofstream out(argv[2]);
        out << "{\"vertices\":" << n << ",\"group_size_mantissa\":" << stats.grpsize1
            << ",\"group_size_exponent\":" << stats.grpsize2 << ",\"generators\":[";
        for (size_t i=0; i<generators.size(); ++i) {
            if (i) out << ',';
            out << '[';
            for (int j=0; j<n; ++j) { if (j) out << ','; out << generators[i][j]; }
            out << ']';
        }
        out << "]}\n";
        if (!out) throw std::runtime_error("Could not write output");
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
