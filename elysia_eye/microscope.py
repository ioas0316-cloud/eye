import numpy as np
from scipy.io import wavfile
import plotly.graph_objects as go

class PhaseMicroscope:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def measure_resonance(self, trajectory):
        """
        Measures resonance based on distance to Love X (0,0,0) and phase balance.
        trajectory: (N, 3) array
        """
        # Distance from origin (x, y) indicates imbalance in 3-phase sum
        imbalance = np.sqrt(trajectory[:, 0]**2 + trajectory[:, 1]**2)
        mean_imbalance = np.mean(imbalance)

        # Harmony is inverse of imbalance
        harmony = 1.0 / (1.0 + mean_imbalance)
        return harmony, imbalance

    def generate_resonance_audio(self, imbalance, duration=2.0):
        """
        Converts imbalance trajectory into audio.
        Low imbalance -> Pure Sine (Harmony)
        High imbalance -> FM/Noise (Friction)
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration))

        # Base frequency (e.g., 440Hz)
        base_freq = 440.0

        # Use imbalance to modulate frequency and add noise
        # Stretch imbalance to match audio duration
        imbalance_stretched = np.interp(t, np.linspace(0, duration, len(imbalance)), imbalance)

        # Harmony: Pure carrier
        # Friction: Modulated carrier + white noise
        carrier = np.sin(2 * np.pi * base_freq * t + 5.0 * np.cumsum(imbalance_stretched) / self.sample_rate)

        noise = np.random.normal(0, 0.1, len(t)) * imbalance_stretched

        audio = carrier + noise
        # Normalize to 16-bit range
        audio = (audio / np.max(np.abs(audio)) * 32767).astype(np.int16)

        return audio

    def visualize_trajectory(self, trajectory, title="Elysia-Eye Trajectory"):
        fig = go.Figure(data=[go.Scatter3d(
            x=trajectory[:, 0],
            y=trajectory[:, 1],
            z=trajectory[:, 2],
            mode='lines',
            line=dict(
                color=np.arange(len(trajectory)),
                colorscale='Viridis',
                width=4
            )
        )])

        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='Phase X',
                yaxis_title='Phase Y',
                zaxis_title='Time / Sequence',
                bgcolor="black"
            ),
            template="plotly_dark"
        )
        return fig

if __name__ == "__main__":
    micro = PhaseMicroscope()
    test_traj = np.random.rand(100, 3)
    harmony, imb = micro.measure_resonance(test_traj)
    audio = micro.generate_resonance_audio(imb)
    print(f"Harmony score: {harmony}")
