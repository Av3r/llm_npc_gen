import subprocess
import sys

def run_test_commands():
    story_file = "data/fantasy.md"

    commands = [
        [sys.executable, "npc_gen/cli.py", "--story-file", story_file, "--story-understanding", "What factions exist?"],
        [sys.executable, "npc_gen/cli.py", "--story-file", story_file, "--generate-hero"],
        [sys.executable, "npc_gen/cli.py", "--story-file", story_file, "--generate-details", "Aldric Stormwind"]
    ]

    for cmd in commands:
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        print("-" * 40)

if __name__ == "__main__":
    run_test_commands()