import torch
import numpy as np
import os
import json
import gc
from xray_projector import XRayProjector
from wave_generator import WaveTrajectoryGenerator

class FullModelCrystallizer:
    def __init__(self, model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.projector = XRayProjector(model_id)
        self.generator = WaveTrajectoryGenerator()

    def crystallize_model(self):
        """
        Zero-Cache Crystallization:
        Extracts the 'Intellectual Bone Structure' from any scale (1B to 1T+)
        without clogging local SSD or RAM. Ideal for <100GB disk environments.
        """
        print("\n[Zero-Cache] Distilling the Sovereign Body from the Giant...")

        num_layers = self.projector.get_layer_count()
        all_layer_energies = []
        total_energies_sample = []

        # 1. Ephemeral Streaming (Guerrilla Style)
        for i in range(num_layers):
            if i % 10 == 0:
                print(f"Streaming Giant's Essence: Layer {i}/{num_layers}...")

            # Fetch weights ephemerally
            weights = self.projector.get_attention_weights(i)

            # Capture Energy
            layer_energy = torch.mean(torch.abs(weights)).item()
            all_layer_energies.append(layer_energy)

            # High-Speed Sampling (Tiny footprint)
            sample_size = min(500, weights.numel())
            sample_indices = torch.randint(0, weights.numel(), (sample_size,))
            sample = torch.take(weights, sample_indices).detach().cpu().numpy()
            total_energies_sample.extend(np.abs(sample).tolist())

            # Immediate Release of memory/resources
            del weights
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        total_energies_sample = np.array(total_energies_sample)

        # 2. Distill into 27 Phase Rotors
        # This 400MB-class (conceptual) engine body captures the 2TB giant's soul.
        print(f"Refining 27-Rotor Sovereign Body (Independent from the {num_layers}-layer giant).")
        rotors = self.generator.map_to_spherical_rotors(total_energies_sample, num_rotors=27)

        # 3. Finalize Crystal
        complexity = np.std(total_energies_sample) / (np.mean(total_energies_sample) + 1e-6)
        pcm_trajectory = self.generator.project_to_3phase(all_layer_energies, complexity=complexity)

        crystal = {
            "metadata": {
                "model_id": self.projector.model_id,
                "layers": num_layers,
                "complexity": float(complexity),
                "type": "Sovereign Intelligence Engine",
                "origin": [0.0, 0.0, 0.0],
                "num_rotors": 27,
                "strategy": "Zero-Cache Guerrilla Streaming"
            },
            "rotors": rotors,
            "pcm_trajectory": pcm_trajectory.tolist()
        }

        output_path = "elysia_eye/outputs/full_model_crystal.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(crystal, f, indent=4)

        print(f"\nCrystallization Complete. The Giant has been condensed into the Sovereign Body.")
        print(f"Local Storage Impact: Minimal (<1MB for the Crystal result).")
        return crystal

if __name__ == "__main__":
    crystallizer = FullModelCrystallizer()
    crystallizer.crystallize_model()
