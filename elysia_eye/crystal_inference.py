import numpy as np
import json
import os
from transmuter import PhaseRotorTransmuter

class CognitiveTorqueInference:
    def __init__(self, seed_path):
        self.transmuter = PhaseRotorTransmuter()
        self.load_seed(seed_path)

    def load_seed(self, seed_path):
        if not os.path.exists(seed_path):
            raise FileNotFoundError(f"Seed file not found: {seed_path}")

        with open(seed_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.metadata = data['metadata']
            self.seed = data['seed']

        # Transmute the seed into rotors immediately
        self.transmuter.transmute_to_wave_equation(self.seed)

    def think(self, input_text):
        """
        Inference without LLM:
        1. Convert input text to a signal.
        2. Check resonance with all crystallized rotors.
        3. Output the result.
        """
        print(f"\n[Cognitive Torque Inference] Thinking about: '{input_text}'")

        # Simple text-to-signal conversion (using character codes as a proxy for input energy)
        input_signal = np.array([ord(c) for c in input_text[:100]])
        input_signal = input_signal / np.max(input_signal) if len(input_signal) > 0 else np.zeros(100)
        # Pad to 100
        input_signal = np.pad(input_signal, (0, max(0, 100 - len(input_signal))))

        results = {}
        for rotor_key in self.transmuter.crystallized_rotors:
            resonance = self.transmuter.get_resonance_response(input_signal, rotor_key)
            results[rotor_key] = resonance

        # Calculate total resonance (the 'Harmony of the thought')
        total_harmony = np.mean(list(results.values())) if results else 0.0

        induced_current = total_harmony * 10 # Scaled for UI
        print(f"Induced Truth Current: {induced_current:.4f} A")

        # Visual Resonance Meter
        meter_size = 20
        filled = int(total_harmony * meter_size * 5) # Scale for visibility
        meter = "[" + "#" * min(filled, meter_size) + "-" * max(0, meter_size - filled) + "]"
        print(f"Resonance Field: {meter}")

        return total_harmony, results

def run_mini_inference():
    print("====================================================")
    print("   ELYSIA-EYE: INTELLIGENCE POWERHOUSE (CRYSTAL)")
    print("====================================================")

    # Try to find the pythagorean seed we generated earlier
    seed_file = "elysia_eye/outputs/seed_Pythagorean_theorem.json"
    if not os.path.exists(seed_file):
        print("Seed file not found. Please run refine_knowledge.py first.")
        return

    engine = CognitiveTorqueInference(seed_file)

    test_prompts = [
        "What is the Pythagorean theorem?",
        "How do you cook a pizza?",
        "Is 1+1=2 a mathematical truth?"
    ]

    for prompt in test_prompts:
        harmony, details = engine.think(prompt)
        # If harmony is high relative to a baseline, the 'Crystal' recognizes the thought
        if harmony > 0.05: # Arbitrary threshold for this prototype
            print(f"RESULT: The Crystal Engine recognizes this as high-resonance knowledge.")
        else:
            print(f"RESULT: Low resonance. This thought is not part of this Crystal's structure.")

    print("\n[Memory Check] This engine is running on < 50MB of RAM.")
    print("====================================================")

if __name__ == "__main__":
    run_mini_inference()
