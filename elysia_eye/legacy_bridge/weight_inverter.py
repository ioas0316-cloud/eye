import torch
import json
import os

class WeightInverter:
    def __init__(self, crystal_path="elysia_eye/outputs/full_model_crystal.json"):
        with open(crystal_path, "r", encoding="utf-8") as f:
            self.crystal = json.load(f)

    def invert_to_adapter(self, target_dim=4096):
        """
        Inverts the spherical phase data back into a weight matrix
        that can be used as a LoRA-like adapter.
        """
        print(f"[Weight Inverter] Mapping Phase parameters back to {target_dim} weight space...")

        rotors = self.crystal['rotors']
        num_rotors = len(rotors)

        # Create a synthetic weight vector based on rotor parameters
        # In a real scenario, this would use the original mapping's inverse.
        inverted_weights = torch.zeros(target_dim)

        chunk_size = target_dim // num_rotors
        for i, r in enumerate(rotors):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, target_dim)

            p = r['params']
            # Reconstruct 'pseudo-weights' from amplitude and phase
            # This is the 'Phase-to-Weight' bridge
            val = p['amp'] * torch.cos(torch.tensor(p['phi']))
            inverted_weights[start:end] = val

        print(f"Inversion complete. Reconstructed weight vector norm: {torch.norm(inverted_weights):.4f}")

        # Save as a simulated adapter file
        output_path = "elysia_eye/outputs/elysia_adapter.pt"
        torch.save(inverted_weights, output_path)
        print(f"Adapter saved to: {output_path}")
        return inverted_weights

if __name__ == "__main__":
    inverter = WeightInverter()
    inverter.invert_to_adapter()
