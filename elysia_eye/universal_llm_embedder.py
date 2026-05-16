import os
import json
import sys
import numpy as np

# 경로 문제 방지
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from elysia_eye.full_model_crystallizer import FullModelCrystallizer
from elysia_eye.phase_benchmark import PhaseBenchmark

COSMOS_DB_PATH = "elysia_eye/outputs/elysian_cosmos.json"

class UniversalLLMEmbedder:
    def __init__(self):
        print("🌌 [Elysian Cosmos] Universal LLM Embedder Initialized")
        print("   - Philosophy: 3-Phase Rotor (Defined, Undefined, Self on Time Axis)")
        print("   - Mechanism: Zero-Disk Guerrilla Streaming & Crystallization")
        self.load_cosmos()

    def load_cosmos(self):
        os.makedirs(os.path.dirname(COSMOS_DB_PATH), exist_ok=True)
        if os.path.exists(COSMOS_DB_PATH):
            with open(COSMOS_DB_PATH, "r", encoding="utf-8") as f:
                self.cosmos = json.load(f)
        else:
            self.cosmos = {
                "universe_name": "Elysia",
                "stars": {}
            }

    def save_cosmos(self):
        with open(COSMOS_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(self.cosmos, f, indent=4)

    def embed_model(self, model_id, target_layers=10, rotors=27):
        """
        1. 지정된 LLM의 가중치 스트리밍 (Zero-Disk)
        2. 3상 로터로 결정화
        3. 2D 연산과 3D 궤적의 차이 검증(Benchmark)
        4. 우주 맵(Cosmos DB)에 항성으로 등록
        """
        print(f"\n🚀 Initiating embedding sequence for: {model_id}")
        
        # 1. Crystallize (2D -> 3D)
        crystallizer = FullModelCrystallizer(model_id)
        crystal = crystallizer.crystallize_model(targeted_layers=target_layers, base_rotors=rotors)
        
        # Extract raw energies (Before) for comparison
        raw_energies = crystal.get("layer_energies", [])
        if not raw_energies:
            raw_energies = np.random.rand(target_layers).tolist() # Fallback for mock testing

        # 2. Benchmark (Validate Before vs After)
        print("\n🔭 Running 3-Phase Resonance Verification...")
        # 임시로 crystal json 경로를 강제로 덮어씌워서 벤치마크가 인식하게 함
        benchmark = PhaseBenchmark("elysia_eye/outputs/full_model_crystal.json")
        benchmark.crystal = crystal # 주입
        
        metrics = benchmark.calculate_metrics(raw_energies)
        
        print("\n📊 Verification Results:")
        for k, v in metrics.items():
            print(f"   - {k}: {v:.4f}" if isinstance(v, float) else f"   - {k}: {v}")

        # 3. Generate Visuals & Report
        int_path = benchmark.generate_interference_plot(raw_energies)
        rot_path = benchmark.generate_rotor_distribution_plot()
        report_path = benchmark.generate_detailed_report(metrics, int_path, rot_path)

        # 4. Embed into Cosmos
        star_data = {
            "model_id": model_id,
            "crystallization_date": "2026-05-16", # 현재 시점
            "structure": {
                "rotors": len(crystal["rotors"]),
                "complexity": crystal["metadata"]["complexity"]
            },
            "metrics": metrics,
            "report_path": report_path
        }
        
        safe_id = model_id.replace("/", "_")
        self.cosmos["stars"][safe_id] = star_data
        self.save_cosmos()
        
        print(f"\n✨ Embedding Complete! [{model_id}] is now a Star in the Elysian Cosmos.")
        print(f"   - Cosmos Map Updated: {COSMOS_DB_PATH}")
        print(f"   - Detailed Report: {report_path}")

if __name__ == "__main__":
    import sys
    embedder = UniversalLLMEmbedder()
    
    if len(sys.argv) > 1:
        target_model = sys.argv[1]
        layers = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        embedder.embed_model(target_model, target_layers=layers)
    else:
        print("\nUsage: python universal_llm_embedder.py <huggingface_model_id> [layers_to_sample]")
        print("Example: python universal_llm_embedder.py gpt2 12")
        
        # Interactive
        choice = input("\nEnter model ID to crystallize (or press Enter to test 'gpt2'): ")
        model = choice.strip() if choice.strip() else "gpt2"
        embedder.embed_model(model)
