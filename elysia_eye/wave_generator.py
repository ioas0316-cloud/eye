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

    def map_to_spherical_rotors(self, weights, num_rotors=27):
        """
        Maps high-dim weights to N rotors distributed on a sphere.
        This ensures equal distance from the origin (Love X).
        """
        print(f"Distributing {num_rotors} Phase Rotors on a spherical surface...")

        # Flatten and calculate magnitude
        if isinstance(weights, torch.Tensor):
            flat_w = weights.flatten().detach().cpu().numpy()
        else:
            flat_w = weights.flatten()

        energies = np.abs(flat_w)
        chunks = np.array_split(energies, num_rotors)

        rotors = []

        # Fibonacci Sphere Algorithm for equal distribution
        phi = np.pi * (3. - np.sqrt(5.))  # golden angle in radians

        for i in range(num_rotors):
            y = 1 - (i / float(num_rotors - 1)) * 2  # y goes from 1 to -1
            radius = np.sqrt(1 - y * y)  # radius at y

            theta = phi * i  # golden angle increment

            x = np.cos(theta) * radius
            z = np.sin(theta) * radius

            # Rotor position (x, y, z) on unit sphere
            pos = np.array([x, y, z])

            # Map chunk data to wave parameters
            chunk = chunks[i]
            amplitude = np.mean(chunk)
            frequency = 1.0 + np.std(chunk)
            phase = (np.mean(chunk) % (2 * np.pi))
            torque = np.max(chunk) - np.min(chunk)

            rotors.append({
                "id": i,
                "pos": pos.tolist(),
                "params": {
                    "amp": float(amplitude),
                    "freq": float(frequency),
                    "phi": float(phase),
                    "torque": float(torque)
                }
            })

        return rotors

if __name__ == "__main__":
    gen = WaveTrajectoryGenerator()
    test_energies = np.random.rand(100)
    traj = gen.project_to_3phase(test_energies, complexity=0.5)
    print(f"Generated trajectory with {traj.shape[0]} points.")
