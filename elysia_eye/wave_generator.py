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
        delta = (np.sin(t * 5) * 0.1) * complexity
        phi1 = 0.0 + (t * 2 * np.pi)
        phi2 = phi1 + self.base_angle_rad + delta
        phi3 = phi1 + 2 * self.base_angle_rad - delta
        return phi1, phi2, phi3

    def project_to_3phase(self, energy_values, complexity):
        points = []
        for i, val in enumerate(energy_values):
            t = i / len(energy_values)
            p1, p2, p3 = self.get_rotor_phases(t, complexity)
            x = val * (np.cos(p1) + np.cos(p2) + np.cos(p3))
            y = val * (np.sin(p1) + np.sin(p2) + np.sin(p3))
            z = t * 10
            points.append([x, y, z])
        return np.array(points)

    def map_to_spherical_rotors(self, weights, num_rotors=27, depth=1):
        """
        Maps high-dim weights to N rotors distributed on a sphere.
        Now supports dynamic scaling and Fractal Recursion.
        """
        if depth > 1:
            pass # Keep quiet during deep recursion
        else:
            print(f"Distributing {num_rotors} Phase Rotors on a spherical surface...")

        if isinstance(weights, torch.Tensor):
            flat_w = weights.flatten().detach().cpu().numpy()
        else:
            flat_w = weights.flatten()

        energies = np.abs(flat_w)
        # Ensure num_rotors is not more than energies length
        num_rotors = min(num_rotors, len(energies))
        if num_rotors <= 0: return []

        chunks = np.array_split(energies, num_rotors)
        rotors = []

        phi = np.pi * (3. - np.sqrt(5.))

        # Entropy-based expansion threshold
        def calculate_entropy(data):
            if len(data) <= 1: return 0
            # Simple entropy proxy: std normalized by mean
            return np.std(data) / (np.mean(data) + 1e-6)

        for i in range(num_rotors):
            y = 1 - (i / float(num_rotors - 1)) * 2 if num_rotors > 1 else 0
            radius = np.sqrt(1 - y * y)
            theta = phi * i
            x = np.cos(theta) * radius
            z = np.sin(theta) * radius
            pos = np.array([x, y, z])

            chunk = chunks[i]
            if len(chunk) == 0: continue

            entropy = calculate_entropy(chunk)

            # Fractal Expansion: If entropy is high, split this rotor to capture more "texture"
            if depth < 2 and entropy > 1.2: # Threshold for expansion
                # Sub-split into 9 sub-rotors
                sub_rotors = self.map_to_spherical_rotors(chunk, num_rotors=9, depth=depth+1)
                rotors.append({
                    "id": f"{depth}_{i}",
                    "pos": pos.tolist(),
                    "type": "FractalCluster",
                    "entropy": float(entropy),
                    "sub_rotors": sub_rotors
                })
            else:
                amplitude = np.mean(chunk)
                frequency = 1.0 + np.std(chunk)
                phase = (np.mean(chunk) % (2 * np.pi))
                torque = np.max(chunk) - np.min(chunk)

                rotors.append({
                    "id": f"{depth}_{i}",
                    "pos": pos.tolist(),
                    "type": "AtomicRotor",
                    "entropy": float(entropy),
                    "params": {
                        "amp": float(amplitude),
                        "freq": float(frequency),
                        "phi": float(phase),
                        "torque": float(torque)
                    }
                })

        return rotors

    def suggest_optimal_rotor_scale(self, weights):
        """
        Analyzes the weight distribution and suggests the best rotor count.
        """
        if isinstance(weights, torch.Tensor):
            w = weights.flatten().detach().cpu().numpy()
        else:
            w = weights.flatten()

        complexity = np.std(w) / (np.mean(np.abs(w)) + 1e-6)

        if complexity < 0.5:
            return 27, "Basic (Quiet Resonance)"
        elif complexity < 1.5:
            return 108, "Medium (Active Resonance)"
        else:
            return 432, "High (Intense Fractal Resonance)"

if __name__ == "__main__":
    gen = WaveTrajectoryGenerator()
    test_energies = np.random.rand(5000)
    # Test expansion to 108 rotors (4x 27)
    rotors = gen.map_to_spherical_rotors(test_energies, num_rotors=108)
    print(f"Generated {len(rotors)} base rotor units.")
