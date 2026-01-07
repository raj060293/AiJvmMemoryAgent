#/Applications/MemoryAnalyzer.app/Contents/MacOS
import os
import subprocess
from pathlib import Path


class MatRunner:
    """
    Runs Eclipse MAT in headless mode and produce analysis artifacts.
    """

    def __init__(self, mat_exec: str):
        self.mat_exec = mat_exec

    def run_reports(self, heap_path: str, out_dir: str):
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        self._run("histogram", heap_path, out_dir)
        self._run("dominator_tree", heap_path, out_dir)
        self._run("gc_roots", heap_path, out_dir)


    def _run(self, query: str, heap_path: str, output_dir: str):
        #mat_exec = os.path.join(
        #    os.environ["MAT_HOME"],
        #    "MemoryAnalyzer"
        #)

        cmd = [
            self.mat_exec,
            "-consolelog",
            "-application", "org.eclipse.mat.api.parse",
            "-query", query,
            "-format", "CSV",
            "-output", output_dir,
            heap_path
        ]
        subprocess.run(cmd, check=True)