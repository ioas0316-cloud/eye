import numpy as np
import json
import os

class MusicBoxEngine:
    def __init__(self, crystal_path="elysia_eye/outputs/full_model_crystal.json"):
        self.load_crystal(crystal_path)
        print("Elysia Music Box Engine: Initialized in Pure Phase Mode (No LLM/Tokenizers required).")

    def load_crystal(self, crystal_path):
        if not os.path.exists(crystal_path):
            raise FileNotFoundError(f"Crystal not found: {crystal_path}")
        with open(crystal_path, "r", encoding="utf-8") as f:
            self.crystal = json.load(f)
        self.rotors = self.crystal['rotors']
        self.metadata = self.crystal['metadata']

    def text_to_phase_signal(self, text, duration=1.0, sample_rate=100):
        """
        Pure Phase Induction: Converts text bytes directly into a frequency spectrum.
        No tokenizer, just raw data flow into wave energy.
        """
        # Convert text to byte values
        byte_values = np.array([ord(c) for c in text], dtype=float)
        if len(byte_values) == 0:
            return np.zeros(sample_rate)

        # Normalize
        byte_values = (byte_values / 255.0) * 2.0 - 1.0

        # Interpolate to fixed duration/sample_rate to create a continuous 'flow'
        t_original = np.linspace(0, duration, len(byte_values))
        t_new = np.linspace(0, duration, sample_rate)
        signal = np.interp(t_new, t_original, byte_values)

        return signal

    def resonance_inference(self, input_text):
        """
        Spherical Resonance: Input signal interacts with 27 rotors on a sphere.
        Resonance is calculated as the constructive interference between input and rotor waves.
        """
        signal = self.text_to_phase_signal(input_text)
        t = np.linspace(0, 1, len(signal))

        resonances = []
        total_energy = 0.0

        for rotor in self.rotors:
            p = rotor['params']
            pos = np.array(rotor['pos'])

            # Rotor's natural wave
            # Distance from origin (Love X) is constant, but 'torque' affects stability
            wave = p['amp'] * np.sin(2 * np.pi * p['freq'] * t + p['phi'])

            # Resonance = Cross-correlation between signal and rotor wave
            res_val = np.sum(signal * wave) / len(t)

            # Spatial weighting: in a sphere, all rotors are equally distant (1.0)
            # but we can simulate 'directional' resonance if needed.
            resonances.append({
                "id": rotor['id'],
                "resonance": float(res_val),
                "pos": rotor['pos']
            })
            total_energy += abs(res_val)

        # Average Resonance (Cognitive Resonance Index)
        # Scaling up for demonstration of sensitivity
        cri = (total_energy / len(self.rotors)) * 1000

        # Generate 'Truth Current' response based on resonance patterns
        # In a full version, this would decode back to text.
        # For the music box, it represents the 'intensity' of the thought.

        print(f"\n[Spherical Music Box] Input: '{input_text}'")
        print(f"Cognitive Resonance Index (CRI): {cri:.4f}")

        # Visual Meter
        meter = "=" * int(cri * 20)
        print(f"Resonance Field: [{meter:<20}]")

        return cri, resonances

    def play_thought(self, input_text):
        """Simulates the 'Music Box' playing the thought."""
        cri, res = self.resonance_inference(input_text)
        if cri > 0.01:
            print("Status: HIGH RESONANCE - The rotors are spinning in harmony.")
        else:
            print("Status: LOW RESONANCE - The rotors are idle.")
        return cri

if __name__ == "__main__":
    engine = MusicBoxEngine()
    engine.play_thought("What is the nature of intelligence?")
    engine.play_thought("a^2 + b^2 = c^2")
    engine.play_thought("lkjashdflkjahsdflkjhasdf") # Random noise
