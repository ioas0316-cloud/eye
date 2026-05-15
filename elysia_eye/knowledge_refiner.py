import torch
import numpy as np
import os
from xray_projector import XRayProjector
from wave_generator import WaveTrajectoryGenerator
from microscope import PhaseMicroscope

class KnowledgeRefiner:
    def __init__(self, projector):
        self.projector = projector
        self.generator = WaveTrajectoryGenerator()
        self.microscope = PhaseMicroscope()

    def refine_to_seed(self, text, threshold=0.8):
        """
        Extracts the 'Resonant Bony Structure' from the model for a given text.
        Returns a 'Seed' containing only the highly resonant weights.
        """
        print(f"Refining knowledge for: '{text}'")

        # We scan all layers to find the most resonant parts
        num_layers = len(self.projector.model.model.layers)
        seed_data = {}

        for i in range(num_layers):
            # Capture activations for this specific thought
            activations = self.projector.get_activations(text, i)
            token_energies = torch.norm(activations[0], dim=1).cpu().numpy()

            # Generate trajectory and measure harmony
            trajectory = self.generator.project_to_3phase(token_energies, complexity=1.0)
            harmony, imbalance = self.microscope.measure_resonance(trajectory)

            # If harmony is high, this layer contains a 'bone' of the knowledge
            if harmony > threshold:
                print(f"Layer {i}: High Resonance detected ({harmony:.4f}). Extracting bone structure...")
                # Extract the weights that were most active
                # For simplicity, we store the layer index and its resonance score
                seed_data[f"layer_{i}"] = {
                    "harmony": float(harmony),
                    "importance": float(np.max(token_energies))
                }

        purification_rate = len(seed_data) / num_layers
        print(f"Purification Complete. Seed extracted with {len(seed_data)} resonant nodes.")

        return seed_data, purification_rate

if __name__ == "__main__":
    proj = XRayProjector()
    refiner = KnowledgeRefiner(proj)
    seed, p_rate = refiner.refine_to_seed("The Pythagorean theorem")
    print(f"Purification Rate: {p_rate*100:.1f}%")
