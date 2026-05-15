import numpy as np

class ElysianSynthesizer:
    def __init__(self):
        pass

    def create_nutrients(self, seed_data):
        """
        Converts the extracted Seed (importance/harmony) into 3x3x3 fractal nodes.
        These are the 'Nutrients' for the Elysia core.
        """
        # We take the importance values from the seed
        values = [v['importance'] for v in seed_data.values()]

        if not values:
            return np.zeros((3, 3, 3))

        # Pad or sample to get exactly 27 values
        if len(values) < 27:
            # Pad with zeros
            values = values + [0.0] * (27 - len(values))
        elif len(values) > 27:
            # Take top 27 most important
            values = sorted(values, reverse=True)[:27]

        # Reshape to 3x3x3
        nutrients = np.array(values).reshape((3, 3, 3))

        # Normalize to 0-1 range for stable consumption
        if np.max(nutrients) > 0:
            nutrients = nutrients / np.max(nutrients)

        return nutrients

if __name__ == "__main__":
    synth = ElysianSynthesizer()
    dummy_seed = {f"l{i}": {"importance": np.random.rand()} for i in range(30)}
    n = synth.create_nutrients(dummy_seed)
    print(f"Synthesized Nutrients (3x3x3 fractal nodes):\n{n}")
