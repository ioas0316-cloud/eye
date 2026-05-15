import os
import json
from datetime import datetime

class JournalManager:
    """
    Journal Manager (결정체 기록장):
    Records the history of crystallization events.
    Tracks model, configuration, time, and resulting metrics.
    """
    def __init__(self, journal_path="elysia_eye/journal.json"):
        self.journal_path = journal_path
        self.entries = self.load_entries()

    def load_entries(self):
        if os.path.exists(self.journal_path):
            try:
                with open(self.journal_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_entries(self):
        with open(self.journal_path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=4, ensure_ascii=False)

    def add_entry(self, model_id, config, results):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "model_id": model_id,
            "config": config,
            "results": results
        }
        self.entries.append(entry)
        self.save_entries()
        print(f"[Journal] New entry recorded for {model_id}.")

    def list_entries(self):
        print("\n" + "📜" * 20)
        print(" ELYSIA-EYE: CRYSTALLIZATION JOURNAL")
        print(" " + "📜" * 20)
        if not self.entries:
            print("기록된 결정화 내역이 없습니다.")
            return

        for i, entry in enumerate(self.entries):
            ts = entry['timestamp'].split('T')[0]
            print(f"{i+1}. [{ts}] {entry['model_id']}")
            print(f"   - Config: {entry['config'].get('rotors')} Rotors, {len(entry['config'].get('layers', []))} Layers")
            print(f"   - Result: Complexity {entry['results'].get('complexity', 0):.4f}")
        print("-" * 40)

if __name__ == "__main__":
    journal = JournalManager()
    # Test entry
    # journal.add_entry("Qwen/Qwen1.5-1.8B-Chat", {"rotors": 27, "layers": [10,11,12]}, {"complexity": 0.1234})
    journal.list_entries()
