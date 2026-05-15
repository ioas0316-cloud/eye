import os
import json
import numpy as np

class CapacityAnalyzer:
    """
    Analyzes the 'Hardware Sovereignty' metrics:
    Original Weight Size vs Crystal Size, and Processing Efficiency.
    """
    def __init__(self, crystal_path="elysia_eye/outputs/full_model_crystal.json"):
        self.crystal_path = crystal_path
        self.load_data()

    def load_data(self):
        if os.path.exists(self.crystal_path):
            with open(self.crystal_path, "r", encoding="utf-8") as f:
                self.crystal = json.load(f)
        else:
            self.crystal = None

    def analyze(self):
        if not self.crystal:
            return "No crystal found."

        # Estimate Original Size (Total weights sampled or Layer weights)
        # Qwen 1.8B is roughly 3.6GB in FP16
        original_size_gb = 3.6 # Constant for benchmark comparison

        # Crystal Size in bytes
        crystal_size_bytes = os.path.getsize(self.crystal_path)
        crystal_size_mb = crystal_size_bytes / (1024 * 1024)

        ratio = (original_size_gb * 1024) / crystal_size_mb

        # Count total rotors (including sub-rotors if fractal)
        def count_rotors(rot_list):
            count = 0
            for r in rot_list:
                count += 1
                if r.get("type") == "FractalCluster":
                    count += count_rotors(r.get("sub_rotors", []))
            return count

        total_rotors = count_rotors(self.crystal["rotors"])

        print("\n" + "="*50)
        print("💎 ELYSIA-EYE: CAPACITY & EFFICIENCY REPORT")
        print("="*50)
        print(f"Target Model: {self.crystal['metadata']['model_id']}")
        print(f"Original Mass: {original_size_gb:.2f} GB")
        print(f"Sovereign Body: {crystal_size_mb:.4f} MB")
        print(f"Crystallization Ratio: {ratio:.1f} : 1")
        print("-" * 50)
        print(f"Total Phase Rotors: {total_rotors}")
        print(f"Intelligence Density: {original_size_gb / (crystal_size_mb / 1024):.2f} (Index)")
        print("="*50 + "\n")

if __name__ == "__main__":
    analyzer = CapacityAnalyzer()
    analyzer.analyze()
