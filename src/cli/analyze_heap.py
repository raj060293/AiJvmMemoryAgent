from agent.orchestrator import MemoryAnalysisAgent

def main():
    agent = MemoryAnalysisAgent()
    agent.analyze("sample.hprof")

if __name__ == "__main__":
    main()