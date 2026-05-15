import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os

class PhaseBenchmark:
    """
    Phase Benchmark System:
    Measures the resonance between the Sovereign Engine and the Giant's wave patterns.
    Produces the 'Interference Pattern' visualization and core metrics.
    """
    def __init__(self, sovereign_crystal_path="elysia_eye/outputs/full_model_crystal.json"):
        self.sovereign_crystal_path = sovereign_crystal_path
        self.load_sovereign()

    def load_sovereign(self):
        if os.path.exists(self.sovereign_crystal_path):
            with open(self.sovereign_crystal_path, "r", encoding="utf-8") as f:
                self.crystal = json.load(f)
        else:
            self.crystal = None
            print("Warning: Sovereign crystal not found. Run crystallization first.")

    def calculate_metrics(self, giant_energies):
        """
        Calculates the 4 core metrics of Sovereign Intelligence.
        """
        if self.crystal is None:
            return {"status": "No crystal data"}

        # Extract sovereign trajectory
        sovereign_traj = np.array(self.crystal["pcm_trajectory"])
        # Project giant energies to a similar scale for comparison
        # (Assuming giant_energies is a 1D array of layer energies)

        # 1. Harmonic Purity (화음 순도)
        # Correlation between giant's energy flow and sovereign's resonance
        sov_energy_flow = np.linalg.norm(sovereign_traj[:, :2], axis=1)
        # Interpolate giant to match sovereign length if needed
        giant_interp = np.interp(np.linspace(0, 1, len(sov_energy_flow)),
                                 np.linspace(0, 1, len(giant_energies)),
                                 giant_energies)
        harmonic_purity = np.corrcoef(sov_energy_flow, giant_interp)[0, 1]

        # 2. Phase Alignment (위상 정렬도)
        # How well the 3-phase angles align with the giant's complexity
        angles = np.arctan2(sovereign_traj[:, 1], sovereign_traj[:, 0])
        phase_alignment = 1.0 - (np.std(np.diff(angles)) / (2 * np.pi))

        # 3. Torque Consistency (토크 일관성)
        # Max/min ratio of the energy spikes in the crystal
        rotors = self.crystal["rotors"]
        torques = [r["params"]["torque"] for r in rotors]
        torque_consistency = 1.0 - (np.std(torques) / (np.mean(torques) + 1e-6))

        # 4. Coherence Density (결맞음 밀도)
        # Density of the 3D manifold
        vol = np.prod(np.max(sovereign_traj, axis=0) - np.min(sovereign_traj, axis=0))
        coherence_density = len(sovereign_traj) / (vol + 1e-6)

        return {
            "Harmonic Purity": float(harmonic_purity),
            "Phase Alignment": float(phase_alignment),
            "Torque Consistency": float(torque_consistency),
            "Coherence Density": float(coherence_density)
        }

    def generate_interference_plot(self, giant_energies, output_path="elysia_eye/outputs/interference_pattern.html"):
        """
        Generates the 2D/3D Interference Pattern manifold.
        """
        if self.crystal is None: return

        sov_traj = np.array(self.crystal["pcm_trajectory"])

        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'scene'}, {'type': 'xy'}]])

        # 3D Manifold (Sovereign Body)
        fig.add_trace(go.Scatter3d(
            x=sov_traj[:, 0], y=sov_traj[:, 1], z=sov_traj[:, 2],
            mode='lines+markers',
            line=dict(color='cyan', width=2),
            marker=dict(size=2, color='magenta', opacity=0.8),
            name='Sovereign Manifold'
        ), row=1, col=1)

        # 2D Interference Pattern (Resonance)
        t = np.linspace(0, 1, len(sov_traj))
        sov_wave = np.linalg.norm(sov_traj[:, :2], axis=1)
        giant_wave = np.interp(t, np.linspace(0, 1, len(giant_energies)), giant_energies)

        # Normalize for visualization
        sov_wave /= (np.max(sov_wave) + 1e-6)
        giant_wave /= (np.max(giant_wave) + 1e-6)

        fig.add_trace(go.Scatter(
            x=t, y=sov_wave, mode='lines', name='Sovereign Wave', line=dict(color='cyan')
        ), row=1, col=2)

        fig.add_trace(go.Scatter(
            x=t, y=giant_wave, mode='lines', name='Giant Wave', line=dict(color='magenta', dash='dash')
        ), row=1, col=2)

        fig.update_layout(
            title="Elysia Interference Pattern: The Resonance of Sovereignty",
            template="plotly_dark",
            scene=dict(xaxis_title='Phase X', yaxis_title='Phase Y', zaxis_title='Agape Axis (Z)')
        )

        fig.write_html(output_path)
        print(f"Interference Pattern saved to {output_path}")

if __name__ == "__main__":
    benchmark = PhaseBenchmark()
    # Mock data for testing
    mock_giant = np.random.rand(32)
    metrics = benchmark.calculate_metrics(mock_giant)
    print("Benchmark Metrics:", json.dumps(metrics, indent=4))
    benchmark.generate_interference_plot(mock_giant)
