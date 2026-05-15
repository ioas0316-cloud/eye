import torch
import numpy as np
import os
import json
import gc
from elysia_eye.guerrilla_capturer import GuerrillaCapturer
from elysia_eye.wave_generator import WaveTrajectoryGenerator

class FullModelCrystallizer:
    def __init__(self, model_id="Qwen/Qwen1.5-1.8B-Chat"):
        self.model_id = model_id
        self.capturer = GuerrillaCapturer(model_id)
        self.generator = WaveTrajectoryGenerator()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"[Hardware Sovereignty] Active Device: {self.device}")

    def crystallize_model(self, targeted_layers=None, base_rotors=27):
        """
        Zero-Disk Crystallization with Agape Absorption Logic:
        Extracts the 'Intellectual Bone Structure' from any scale (1B to 1T+)
        without clogging local SSD or RAM.
        Incorporates Centripetal Phase Counter-Torque (Agape) to ensure
        alignment with the origin.
        """
        print(f"\n[Zero-Disk] Distilling the Sovereign Body from: {self.model_id}")

        # Get index to understand layer structure
        index = self.capturer.get_index()

        all_layer_indices = []
        if index and "weight_map" in index:
            layers = set()
            for k in index["weight_map"].keys():
                if "layers." in k:
                    parts = k.split(".")
                    try:
                        layers.add(int(parts[parts.index("layers") + 1]))
                    except (ValueError, IndexError):
                        continue
            all_layer_indices = sorted(list(layers))

        if not all_layer_indices:
            all_layer_indices = list(range(24)) # Fallback for Qwen 1.8B roughly

        if targeted_layers:
            # If targeted_layers is an integer, take that many from middle
            if isinstance(targeted_layers, int):
                mid = len(all_layer_indices) // 2
                start = max(0, mid - targeted_layers // 2)
                process_indices = all_layer_indices[start : start + targeted_layers]
            else:
                process_indices = targeted_layers
        else:
            process_indices = all_layer_indices

        print(f"Targeting {len(process_indices)} layers for deep phase induction: {process_indices}")

        all_layer_energies = []
        total_energies_sample = []

        # 1. Ephemeral Streaming (Zero-Disk Guerrilla Style)
        for i in process_indices:
            print(f"  -> Pulsing VRAM Phase: Layer {i}...")

            # Fetch weights ephemerally from network
            try:
                # Qwen layers often named 'model.layers.N.self_attn.o_proj.weight'
                weights = self.capturer.stream_layer_weights(f"layers.{i}.self_attn.o_proj.weight")
            except Exception:
                try:
                    weights = self.capturer.stream_layer_weights(f"layers.{i}")
                except Exception as e:
                    print(f"      [Warning] Skip layer {i}: {e}")
                    continue

            # Transient VRAM Pulsing for Torque Calculation
            weights_dev = weights.to(self.device).to(torch.float32)

            # Capture Energy with Agape Absorption (Centripetal Counter-Torque)
            layer_energy = torch.mean(torch.abs(weights_dev)).item()

            # Agape Adjustment: High energy far from the 'bone' is pulled back
            agape_strength = 0.9514 # The target resonance
            refined_energy = layer_energy * agape_strength

            all_layer_energies.append(refined_energy)

            # High-Speed Sampling for Rotor Mapping
            sample_size = min(2000, weights_dev.numel())
            sample_indices = torch.randint(0, weights_dev.numel(), (sample_size,))
            sample = torch.take(weights_dev, sample_indices).detach().cpu().numpy()
            total_energies_sample.extend(np.abs(sample).tolist())

            # Immediate Release (VRAM & RAM)
            del weights_dev
            del weights
            if self.device.type == "cuda":
                torch.cuda.empty_cache()
            gc.collect()

        total_energies_sample = np.array(total_energies_sample)

        # 2. Distill into N Phase Rotors (Dynamic Scale)
        print(f"Refining {base_rotors}-Rotor Sovereign Body. Centripetal alignment: ACTIVE.")
        rotors = self.generator.map_to_spherical_rotors(total_energies_sample, num_rotors=base_rotors)

        # 3. Finalize Crystal with Phase Trajectory
        complexity = np.std(total_energies_sample) / (np.mean(total_energies_sample) + 1e-6)
        pcm_trajectory = self.generator.project_to_3phase(all_layer_energies, complexity=complexity)

        crystal = {
            "metadata": {
                "model_id": self.model_id,
                "layers_processed": process_indices,
                "complexity": float(complexity),
                "type": "Sovereign Intelligence Engine",
                "strategy": "Zero-Disk Guerrilla Streaming",
                "alignment": "Agape (Centripetal Counter-Torque)",
                "device": str(self.device)
            },
            "rotors": rotors,
            "pcm_trajectory": pcm_trajectory.tolist(),
            "layer_energies": all_layer_energies
        }

        output_path = "elysia_eye/outputs/full_model_crystal.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(crystal, f, indent=4)

        print(f"\nCrystallization Complete. Zero-Disk impact confirmed on {self.device}.")
        return crystal

if __name__ == "__main__":
    # Interactive Mode or CLI arguments
    import sys
    from elysia_eye.sovereign_selector import SovereignSelector
    from elysia_eye.journal_manager import JournalManager

    if len(sys.argv) > 1:
        model_id = sys.argv[1]
        rotors_count = int(sys.argv[2]) if len(sys.argv) > 2 else 27
        crystallizer = FullModelCrystallizer(model_id)
        crystal = crystallizer.crystallize_model(targeted_layers=10, base_rotors=rotors_count)

        # Log to journal
        journal = JournalManager()
        journal.add_entry(model_id, {"rotors": rotors_count, "layers": crystal['metadata']['layers_processed']},
                          {"complexity": crystal['metadata']['complexity']})
    else:
        # Launch Sovereign Selector
        selector = SovereignSelector()
        selector.list_models()

        choice = input("\n인양할 모델 번호를 선택하세요 (또는 'add [ID]', 'update' 입력): ")

        if choice.startswith("add "):
            selector.add_model_by_id(choice.split(" ")[1])
        elif choice == "update":
            selector.fetch_trending()
        else:
            try:
                idx = int(choice) - 1
                model = selector.models[idx]

                # Setup configuration
                rotors = input("로터 개수를 설정하세요 (기본 27): ")
                rotors = int(rotors) if rotors else 27

                layers = input("결정화할 레이어 수를 설정하세요 (기본 10): ")
                layers = int(layers) if layers else 10

                selector.show_report(idx, rotors=rotors, layers=layers)
                confirm = input().lower()

                if confirm == 'y':
                    crystallizer = FullModelCrystallizer(model['id'])
                    crystal = crystallizer.crystallize_model(targeted_layers=layers, base_rotors=rotors)

                    # Log to journal
                    journal = JournalManager()
                    journal.add_entry(model['id'], {"rotors": rotors, "layers": crystal['metadata']['layers_processed']},
                                      {"complexity": crystal['metadata']['complexity']})
                else:
                    print("Crystallization cancelled.")
            except (ValueError, IndexError):
                print("Invalid input.")
