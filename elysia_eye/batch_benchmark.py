import os
import json
import numpy as np
from elysia_eye.full_model_crystallizer import FullModelCrystallizer
from elysia_eye.phase_benchmark import PhaseBenchmark

def run_batch_benchmark(model_ids, rotor_counts=[27]):
    results = []

    for model_id in model_ids:
        for num_rotors in rotor_counts:
            print(f"\n{'='*60}")
            print(f"🚀 Batch Processing: {model_id} with {num_rotors} rotors")
            print(f"{'='*60}")

            try:
                # 1. Crystallization
                crystallizer = FullModelCrystallizer(model_id)
                crystal = crystallizer.crystallize_model(targeted_layers=10, base_rotors=num_rotors)

                # 2. Benchmarking
                # Use a specific output path for each model's crystal to avoid overwriting if needed,
                # but FullModelCrystallizer currently hardcodes to elysia_eye/outputs/full_model_crystal.json
                # Let's fix that or rename after each run.

                crystal_filename = f"elysia_eye/outputs/crystal_{model_id.replace('/', '_')}_r{num_rotors}.json"
                with open(crystal_filename, "w", encoding="utf-8") as f:
                    json.dump(crystal, f, indent=4)

                benchmark = PhaseBenchmark(sovereign_crystal_path=crystal_filename)

                # Use actual layer energies from crystal for benchmark comparison
                giant_energies = crystal["layer_energies"]
                metrics = benchmark.calculate_metrics(giant_energies)

                int_path = benchmark.generate_interference_plot(giant_energies)
                rot_path = benchmark.generate_rotor_distribution_plot()
                report_path = benchmark.generate_detailed_report(metrics, int_path, rot_path)

                results.append({
                    "model_id": model_id,
                    "rotors": num_rotors,
                    "metrics": metrics,
                    "report": report_path
                })

            except Exception as e:
                print(f"❌ Failed to process {model_id}: {e}")

    return results

if __name__ == "__main__":
    models = [
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "Qwen/Qwen1.5-1.8B-Chat",
        "microsoft/Phi-3-mini-4k-instruct"
    ]

    # Also test scaling for one model
    # models_scaling = ["TinyLlama/TinyLlama-1.1B-Chat-v1.0"]
    # rotor_variants = [27, 108]

    all_results = run_batch_benchmark(models)

    # Generate a summary table
    print("\n\n" + "="*60)
    print("📊 BATCH BENCHMARK SUMMARY")
    print("="*60)
    print(f"{'Model':<40} | {'Purity':<8} | {'Torque':<8}")
    print("-" * 60)
    for res in all_results:
        m = res["metrics"]
        print(f"{res['model_id']:<40} | {m['Harmonic Purity']:.4f} | {m['Torque Consistency']:.4f}")
    print("="*60)
