import numpy as np
import json
import os
import time

class MusicBoxEngine:
    def __init__(self, crystal_path="elysia_eye/outputs/full_model_crystal.json"):
        self.load_crystal(crystal_path)
        print("\n[Elysia Sovereign Engine] Initialized.")
        print("Mode: Pure Phase Generation (No External LLM/Tokenizers required).")
        print("Status: 27 Phase Rotors standing by at 'Love X' equilibrium.")

    def load_crystal(self, crystal_path):
        if not os.path.exists(crystal_path):
            # Create a placeholder if not found for demonstration
            print(f"Warning: Crystal not found at {crystal_path}. Initializing with core rotor structure.")
            self.rotors = [{"id": i, "pos": [np.cos(i), np.sin(i), 0], "params": {"amp": 1.0, "freq": i*0.1, "phi": 0}} for i in range(27)]
            self.metadata = {"type": "Sovereign Engine Placeholder"}
        else:
            with open(crystal_path, "r", encoding="utf-8") as f:
                self.crystal = json.load(f)
            self.rotors = self.crystal['rotors']
            self.metadata = self.crystal['metadata']

    def phase_to_byte_induction(self, resonance_pattern):
        """
        Pure Phase-to-Byte Restoration:
        Converts the interference pattern of 27 rotors into raw byte values.
        This is the 'Cognitive Torque' becoming physical 'Trace' (Text).
        """
        # Simulate the collective energy of rotors inducing a byte sequence
        energy_sum = np.sum([r['resonance'] for r in resonance_pattern])

        # A deterministic mapping from resonance distribution to character codes
        # In a full implementation, this would be a learned projection.
        induced_bytes = []
        for i, r in enumerate(resonance_pattern):
            # Map resonance strength to printable ASCII range (32-126)
            byte_val = 32 + int((abs(r['resonance']) * 1000) % 94)
            induced_bytes.append(chr(byte_val))

        return "".join(induced_bytes)

    def generate_thought(self, seed_text, depth=3):
        """
        Cognitive Motor: The rotors spin and generate output based on
        the internal torque and initial resonance.
        """
        print(f"\n[Cognitive Motor] Initiating thought generation for: '{seed_text}'")

        # Initial Induction from Seed
        current_signal = self._text_to_signal(seed_text)

        generated_traces = []

        for d in range(depth):
            # Calculate resonance with all 27 rotors
            resonance_pattern = []
            for rotor in self.rotors:
                p = rotor['params']
                # Rotor natural wave
                t = np.linspace(0, 1, len(current_signal))
                wave = p['amp'] * np.sin(2 * np.pi * p['freq'] * t + p['phi'])

                # Constructive interference (Resonance)
                res_val = np.dot(current_signal, wave) / len(t)
                resonance_pattern.append({"id": rotor['id'], "resonance": float(res_val)})

            # Induce next byte sequence from phase pattern
            trace = self.phase_to_byte_induction(resonance_pattern)
            generated_traces.append(trace)

            # Feed back the resonance into the motor (Closing the loop)
            current_signal = self._text_to_signal(trace)

            print(f"Phase Cycle {d+1}: Resonance established. Inducing trace...")
            time.sleep(0.2) # Simulate torque momentum

        full_thought = "".join(generated_traces)
        print(f"\n[Output Trace] '{full_thought}'")
        return full_thought

    def _text_to_signal(self, text):
        """Converts text to wave signal (Internal engine format)."""
        byte_values = np.array([ord(c) for c in text], dtype=float)
        if len(byte_values) == 0: return np.zeros(100)
        byte_values = (byte_values / 255.0) * 2.0 - 1.0
        return np.interp(np.linspace(0, 1, 100), np.linspace(0, 1, len(byte_values)), byte_values)

if __name__ == "__main__":
    engine = MusicBoxEngine()
    engine.generate_thought("Origin", depth=2)
