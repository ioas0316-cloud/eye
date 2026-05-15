import torch
import numpy as np
import os
import json
from xray_projector import XRayProjector
from wave_generator import WaveTrajectoryGenerator
from archive_manager import SovereignArchive

class FullModelCrystallizer:
    def __init__(self, model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.projector = XRayProjector(model_id)
        self.generator = WaveTrajectoryGenerator()
        self.archive = SovereignArchive()

    def crystallize_model(self):
        """
        Scans the entire model and projects its intelligence
        into 27 Spherical Phase Rotors.
        """
        print("\n[Full Model Crystallization] Starting 'Spherical Intelligence Music Box' assembly...")

        num_layers = len(self.projector.model.model.layers)
        all_layer_energies = []

        # 1. Scan Layers
        for i in range(num_layers):
            print(f"Scanning Layer {i}/{num_layers} for structural bones...")
            weights = self.projector.get_attention_weights(i)
            layer_energy = torch.mean(torch.abs(weights)).item()
            all_layer_energies.append(layer_energy)

        # 2. Extract Global Distribution for Rotors
        print("Sampling global weight distribution for spherical mapping...")
        total_energies = []
        # Sample from a subset of layers to avoid memory issues while maintaining representation
        for i in range(0, num_layers, 2):
            w = self.projector.get_attention_weights(i)
            sample_size = min(2000, w.numel())
            sample_indices = torch.randint(0, w.numel(), (sample_size,))
            sample = torch.take(w, sample_indices)
            total_energies.extend(torch.abs(sample).detach().cpu().numpy().tolist())

        total_energies = np.array(total_energies)

        # 3. Create 27 Spherical Rotors
        rotors = self.generator.map_to_spherical_rotors(total_energies, num_rotors=27)

        # 4. Generate Global PCM (Phase Coordinate Matrix)
        complexity = np.std(total_energies) / (np.mean(total_energies) + 1e-6)
        pcm_trajectory = self.generator.project_to_3phase(all_layer_energies, complexity=complexity)

        crystal = {
            "metadata": {
                "model_id": self.projector.model.config._name_or_path,
                "layers": num_layers,
                "complexity": float(complexity),
                "type": "Spherical Intelligence Music Box",
                "origin": [0.0, 0.0, 0.0], # Love X
                "num_rotors": 27
            },
            "rotors": rotors,
            "pcm_trajectory": pcm_trajectory.tolist()
        }

        output_path = "elysia_eye/outputs/full_model_crystal.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(crystal, f, indent=4)

        print(f"\nCrystallization Complete! Output saved to: {output_path}")
        print(f"Final Music Box Size: ~{os.path.getsize(output_path)/1024:.2f} KB")
        return crystal

if __name__ == "__main__":
    crystallizer = FullModelCrystallizer()
    crystallizer.crystallize_model()
