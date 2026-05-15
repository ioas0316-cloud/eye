import numpy as np
import torch

class WaveTrajectoryGenerator:
    def __init__(self, base_angle=120.0):
        self.base_angle_rad = np.radians(base_angle)
        self.center = np.array([0.0, 0.0, 0.0]) # Love X

    def get_rotor_phases(self, t, complexity):
        """
        Calculates the 3-phase angles with a variable dial (delta).
        delta depends on complexity (C).
        """
        # delta: higher complexity leads to more jitter/deviation from 120 deg
        delta = (np.sin(t * 5) * 0.1) * complexity

        phi1 = 0.0 + (t * 2 * np.pi) # Base rotation
        phi2 = phi1 + self.base_angle_rad + delta
        phi3 = phi1 + 2 * self.base_angle_rad - delta

        return phi1, phi2, phi3

    def project_to_3phase(self, energy_values, complexity):
        """
        Projects energy values (from weights/activations) into 3D space using 3-phase rotors.
        energy_values: 1D array of magnitudes.
        """
        points = []
        for i, val in enumerate(energy_values):
            t = i / len(energy_values)
            p1, p2, p3 = self.get_rotor_phases(t, complexity)

            # 3D Spiral construction
            # x, y are determined by the 3-phase interference
            # z is the time/progression axis

            x = val * (np.cos(p1) + np.cos(p2) + np.cos(p3))
            y = val * (np.sin(p1) + np.sin(p2) + np.sin(p3))
            z = t * 10 # Spread along Z axis

            points.append([x, y, z])

        return np.array(points)

    def map_to_fractal_nodes(self, weights):
        """
        Maps high-dim weights to 3x3x3 fractal nodes based on energy density.
        For simplicity in this first version, we'll partition the weights into 27 groups
        and calculate energy density for each.
        """
        # Flatten and calculate magnitude
        flat_w = weights.flatten().cpu().numpy()
        energies = np.abs(flat_w)

        # Sort or partition into 27 chunks
        chunks = np.array_split(energies, 27)
        node_energies = [np.mean(c) for c in chunks]

        # Reshape to 3x3x3
        fractal_grid = np.array(node_energies).reshape((3, 3, 3))
        return fractal_grid

if __name__ == "__main__":
    gen = WaveTrajectoryGenerator()
    test_energies = np.random.rand(100)
    traj = gen.project_to_3phase(test_energies, complexity=0.5)
    print(f"Generated trajectory with {traj.shape[0]} points.")
