import os
import torch
import numpy as np
from scipy.io import wavfile
from xray_projector import XRayProjector
from wave_generator import WaveTrajectoryGenerator
from microscope import PhaseMicroscope
from archive_manager import SovereignArchive

def run_experiment():
    print("=== Elysia-Eye First Experiment: Pythagorean Theorem ===")

    # 0. Ensure directories exist
    os.makedirs("elysia_eye/outputs", exist_ok=True)
    os.makedirs("elysia_eye/archive", exist_ok=True)

    # 1. Setup
    projector = XRayProjector()
    generator = WaveTrajectoryGenerator()
    microscope = PhaseMicroscope()
    archive = SovereignArchive()

    text = "In a right-angled triangle, the square of the hypotenuse side is equal to the sum of squares of the other two sides. a^2 + b^2 = c^2."

    # 2. Scanning (X-Ray Projection)
    # We'll scan layer 12 (roughly middle of the model)
    target_layer = 12
    print(f"Scanning Attention layer {target_layer} for statement: '{text}'")

    activations = projector.get_activations(text, target_layer)
    # activations shape: [1, seq_len, hidden_size]
    # We'll take the first batch and flatten the features or take mean
    seq_activations = activations[0].cpu().numpy() # [seq_len, hidden_size]

    # Calculate energy (magnitude) per token
    token_energies = np.linalg.norm(seq_activations, axis=1)

    # 3. Wave Trajectory Generation
    print("Generating Wave Trajectory...")
    # Complexity: based on activation variance
    complexity = np.std(token_energies) / np.mean(token_energies)
    trajectory = generator.project_to_3phase(token_energies, complexity=complexity)

    # 4. Analysis (Phase Microscope)
    print("Analyzing Resonance...")
    harmony, imbalance = microscope.measure_resonance(trajectory)
    print(f"Resonance Analysis Result: Harmony = {harmony:.4f}")

    # 5. Visualization & Audio
    print("Creating Visualization and Audio...")
    fig = microscope.visualize_trajectory(trajectory, title=f"Elysia-Eye: Pythagorean Theorem (Layer {target_layer})")
    viz_path = "elysia_eye/outputs/pythagoras_trajectory.html"
    fig.write_html(viz_path)

    audio_data = microscope.generate_resonance_audio(imbalance)
    audio_path = "elysia_eye/outputs/pythagoras_resonance.wav"
    wavfile.write(audio_path, microscope.sample_rate, audio_data)

    # 6. Archive
    archive.store_trajectory("pythagoras_theorem", trajectory, {
        "layer": target_layer,
        "text": text,
        "harmony": harmony
    })

    print(f"\nExperiment Complete!")
    print(f"Visualization: {viz_path}")
    print(f"Audio: {audio_path}")

if __name__ == "__main__":
    run_experiment()
