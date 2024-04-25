# COMP 6651 Algorithm Design Techniques Project - Winter 2024

### Team Members
- Beavan Joe Mathias (40274832)
- Slade Justin Ferrao (40275410)
- Smridhi Verma (40266036)

### Overview
This project encompasses the implementation of various algorithms to process and analyze graph data. The primary functionalities include graph generation, Largest Connected Component (LCC) analysis, and Longest Shortest Path (LSP) calculations using different algorithms.

### Components
- `generateGraph.py`: Generates graphs with 300, 400, and 500 vertices. Graphs are saved in `.edges` and `.mtx` formats.
- `Driver.py`: Serves as the entry point for executing the main functionalities including graph generation, LCC calculations, and LSP algorithm comparisons.
- `DFSLSP.py`: Implements the DFS algorithm for LSP calculations.
- `DijkstraLSP.py`: Implements Dijkstra's algorithm for LSP calculations.
- `AStarLSP.py`: Implements the A* algorithm for LSP calculations.
- `OwnHeuristicLSP.py`: Implements a custom heuristic algorithm for LSP calculations.

### Execution Instructions
1. Ensure Python is installed on your system.
2. Open a Terminal or your preferred IDE.
3. Navigate to the project directory.
4. Execute the `Driver.py` file by running:
```bash
python Driver.py
# or
python3 Driver.py
```
5. Upon execution, a menu will be presented. Follow the on-screen prompts to choose the desired operation.

### Comprehensive Analysis
To perform a comprehensive analysis that includes combined results of all algorithms across all specified graph files, select option 6 from the menu.

This setup facilitates a systematic and detailed examination of algorithmic performance across a variety of graph structures.
