import torch
import numpy as np
import json
import os

class ResonanceGate:
    """
    Resonance Gate:
    A dynamic alternative to static if/else branching.
    Instead of binary thresholds, it uses Phase Resonance (Coherence)
    between the input wave and a target phase rotor.
    """
    def __init__(self, rotor_id=0, crystal_path="elysia_eye/outputs/full_model_crystal.json"):
        self.load_rotor(rotor_id, crystal_path)

    def load_rotor(self, rotor_id, crystal_path):
        if os.path.exists(crystal_path):
            with open(crystal_path, "r", encoding="utf-8") as f:
                crystal = json.load(f)
                self.rotor = crystal["rotors"][rotor_id]
                print(f"[Resonance Gate] Loaded Rotor {rotor_id} from {crystal['metadata']['model_id']}")
        else:
            # Fallback mock rotor if crystal doesn't exist
            self.rotor = {
                "params": {"amp": 0.5, "freq": 1.5, "phi": 0.0, "torque": 0.2}
            }
            print("[Resonance Gate] Warning: Using fallback mock rotor.")

    def calculate_resonance(self, input_wave):
        """
        Calculates the resonance (G) between input and rotor.
        input_wave: a 1D tensor or list representing the signal.
        """
        if isinstance(input_wave, list):
            input_wave = torch.tensor(input_wave, dtype=torch.float32)

        # Target wave from rotor
        t = torch.linspace(0, 1, len(input_wave))
        target_amp = self.rotor["params"]["amp"]
        target_freq = self.rotor["params"]["freq"]
        target_phi = self.rotor["params"]["phi"]

        target_wave = target_amp * torch.cos(target_freq * 2 * np.pi * t + target_phi)

        # Calculate Dot Product / Integration (Resonance)
        # Normalize by the product of norms for a "Coherence" measure (0 to 1)
        # Avoid division by zero
        denom = (torch.norm(input_wave) * torch.norm(target_wave)) + 1e-8
        resonance_score = torch.abs(torch.dot(input_wave, target_wave)) / denom
        return resonance_score.item()

    def process(self, data, threshold_coherence=0.3):
        """
        Replaces 'if data > threshold' with resonance logic.
        """
        # Convert raw data to wave (Phase Induction)
        # We simulate induction by creating a wave from the input sequence
        input_wave = torch.sin(torch.tensor(data, dtype=torch.float32) * 5.0)

        res_score = self.calculate_resonance(input_wave)

        # In this dynamic paradigm, torque consistency from the crystal
        # can influence the sensitivity of the gate.
        is_resonant = res_score > threshold_coherence

        print(f"--- Resonance Evaluation ---")
        print(f"  Input Data: {data}")
        print(f"  Coherence Score: {res_score:.6f}")
        print(f"  Gate Threshold: {threshold_coherence:.6f}")
        print(f"  Status: {'RESONANT (GATE OPEN)' if is_resonant else 'DISSONANT (GATE CLOSED)'}")

        return is_resonant

if __name__ == "__main__":
    gate = ResonanceGate(rotor_id=13) # Use middle-ish rotor

    # Let's find an input that resonates better
    # We'll use the rotor's frequency to generate a "matching" signal
    t = np.linspace(0, 1, 10)
    matching_data = np.cos(gate.rotor["params"]["freq"] * 2 * np.pi * t + gate.rotor["params"]["phi"])

    print("\n[Scenario 1: Harmonious Input (Induced from Rotor)]")
    gate.process(matching_data.tolist(), threshold_coherence=0.6)

    print("\n[Scenario 2: Random Dissonant Input]")
    gate.process(np.random.rand(10).tolist(), threshold_coherence=0.6)
