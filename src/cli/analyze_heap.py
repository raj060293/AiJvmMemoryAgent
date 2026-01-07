import os
import sys

from agent.orchestrator import MemoryAnalysisAgent

def main():

    if (len(sys.argv) < 2):
        print("Usage: analyze_heap.py <heap_dump.hprof>")
        sys.exit(1)

    mat_exec = os.getenv("MAT_EXEC")
    if not mat_exec:
        raise RuntimeError("MAT_EXEC environment variable is not set")

    heap_path = sys.argv[1]
    agent = MemoryAnalysisAgent(mat_exec=mat_exec)
    agent.analyze(heap_path)

if __name__ == "__main__":
    main()