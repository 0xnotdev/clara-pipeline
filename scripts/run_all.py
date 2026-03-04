"""
run_all.py — Batch runner: runs Pipeline A then Pipeline B for all 10 files
"""
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

def run_script(script: str) -> bool:
    print(f"\n{'#'*60}")
    print(f"  Running: {script}")
    print(f"{'#'*60}")
    result = subprocess.run(
        [sys.executable, f"scripts/{script}"],
        capture_output=False
    )
    return result.returncode == 0

def main():
    print("\n" + "="*60)
    print("  Clara Answers — Full Pipeline Run")
    print(f"  Started: {datetime.utcnow().isoformat()}")
    print("="*60)
    
    # Run Pipeline A
    a_ok = run_script("pipeline_a.py")
    if not a_ok:
        print("\n❌ Pipeline A failed. Fix errors before running Pipeline B.")
        sys.exit(1)
    
    # Run Pipeline B
    b_ok = run_script("pipeline_b.py")
    if not b_ok:
        print("\n❌ Pipeline B failed.")
        sys.exit(1)
    
    # Final summary
    print("\n" + "="*60)
    print("  ✅ All pipelines complete!")
    print("="*60)
    
    # Count outputs
    outputs = list(Path("outputs/accounts").glob("*/v*/*.json"))
    changelogs = list(Path("changelog").glob("*.json"))
    tasks = list(Path("outputs/task_tracker").glob("*.json"))
    
    print(f"\n  📁 Output files:    {len(outputs)}")
    print(f"  📋 Changelogs:      {len(changelogs)}")
    print(f"  ✅ Task items:      {len(tasks)}")
    print(f"\n  📂 Browse outputs: outputs/accounts/")
    print(f"  📂 Changelogs:      changelog/")
    print(f"  🌐 Diff viewer:     open dashboard.html in browser")
    print("="*60)

if __name__ == "__main__":
    main()
