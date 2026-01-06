#/Applications/MemoryAnalyzer.app/Contents/MacOS
import os
import subprocess
from pathlib import Path


class MatRunner:
    """
    Runs Eclipse MAT in headless mode and produce analysis artifacts.
    """

    def run(self, heap_path: str, output_dir: str):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        mat_exec = os.path.join(
            os.environ["MAT_HOME"],
            "MemoryAnalyzer"
        )

        cmd = [
            mat_exec,
            "-consolelog",
            "-application", "org.eclipse.mat.api.parse",
            "-data", output_dir,
            heap_path
        ]
        subprocess.run(cmd, check=True)