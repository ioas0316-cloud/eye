import h5py
import numpy as np
import datetime
import os

class SovereignArchive:
    def __init__(self, storage_path="elysia_eye/archive"):
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    def store_trajectory(self, name, trajectory, metadata={}):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.h5"
        filepath = os.path.join(self.storage_path, filename)

        with h5py.File(filepath, 'w') as f:
            dset = f.create_dataset("trajectory", data=trajectory)
            for k, v in metadata.items():
                dset.attrs[k] = v

        print(f"Trajectory stored in Sovereign Archive: {filepath}")
        return filepath

    def list_trajectories(self):
        return os.listdir(self.storage_path)

if __name__ == "__main__":
    archive = SovereignArchive()
    test_traj = np.random.rand(100, 3)
    archive.store_trajectory("pythagoras_test", test_traj, {"layer": 0, "model": "TinyLlama"})
