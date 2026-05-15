import os
import json
import torch
import httpx
from elysia_eye.guerrilla_capturer import GuerrillaCapturer

class SovereignSelector:
    """
    Sovereign Selector (소버린 셀렉터):
    A tool for users to browse, select, and analyze LLMs before crystallization.
    Calculates hardware difficulty and estimates output size.
    """
    def __init__(self, models_file="elysia_eye/models.json"):
        self.models_file = models_file
        self.models = self.load_models()
        self.vram_gb = self.get_vram_info()

    def load_models(self):
        if os.path.exists(self.models_file):
            with open(self.models_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_models(self):
        with open(self.models_file, "w", encoding="utf-8") as f:
            json.dump(self.models, f, indent=4, ensure_ascii=False)

    def get_vram_info(self):
        if torch.cuda.is_available():
            vram_bytes = torch.cuda.get_device_properties(0).total_memory
            return vram_bytes / (1024**3)
        return 0.0

    def calculate_difficulty(self, model_size_gb):
        if self.vram_gb == 0:
            return "Unknown (CPU Mode)"

        # Difficulty logic based on VRAM vs Model Size (streaming context)
        # Even with streaming, higher model size usually means more layers/wider layers
        ratio = model_size_gb / self.vram_gb

        if ratio < 1.0:
            return "⭐⭐ (간식 - 매우 쾌적)"
        elif ratio < 5.0:
            return "⭐⭐⭐ (보통 - 안정적)"
        elif ratio < 20.0:
            return "⭐⭐⭐⭐ (도전 - VRAM 압박 가능성)"
        else:
            return "⭐⭐⭐⭐⭐ (극한 - 정밀한 펄싱 필요)"

    def estimate_crystal_size(self, num_rotors, num_layers):
        # Rough estimation: each rotor and trajectory point takes some space
        # Based on current full_model_crystal.json structure
        # metadata + rotors (list of dicts) + trajectory (list of floats)
        # Roughly 20KB per layer + 5KB per rotor
        base_size_kb = 100
        estimated_kb = base_size_kb + (num_layers * 25) + (num_rotors * 10)
        return estimated_kb / 1024 # return in MB

    def list_models(self):
        print("\n" + "="*70)
        print("🌌 ELYSIA-EYE: SOVEREIGN SELECTOR (지능의 쇼핑 리스트)")
        print("="*70)
        print(f"{'No.':<4} | {'Model Name':<25} | {'Size':<8} | {'Difficulty'}")
        print("-" * 70)
        for i, m in enumerate(self.models):
            diff = self.calculate_difficulty(m['size_gb'])
            print(f"{i+1:<4} | {m['name']:<25} | {m['size_gb']:>5.1f} GB | {diff}")
        print("="*70)

    def add_model_by_id(self, model_id):
        print(f"\n[Surgical Strike] Fetching metadata for: {model_id}...")
        try:
            # Try to get index to estimate size if not provided
            capturer = GuerrillaCapturer(model_id)
            index = capturer.get_index()

            # Simple size estimation from index or HF API
            # For simplicity, we'll use a placeholder or prompt user
            size_gb = 7.0 # Placeholder

            new_model = {
                "name": model_id.split("/")[-1],
                "id": model_id,
                "size_gb": size_gb,
                "description": "사용자가 직접 인양한 모델",
                "tags": ["Custom"],
                "streaming_support": True,
                "recommendation": "직접 검증 필요"
            }
            self.models.append(new_model)
            self.save_models()
            print(f"Successfully added {model_id} to the list!")
        except Exception as e:
            print(f"Failed to add model: {e}")

    def fetch_trending(self):
        print("\n[Auto-Fetch] Scouting Hugging Face for trending waves...")
        # In a real scenario, use httpx to call HF API
        # https://huggingface.co/api/models?sort=downloads&direction=-1&limit=5&filter=text-generation,safetensors
        print("(API Call simulated for now - Adding a trending candidate: Mistral-7B-v0.3)")
        self.add_model_by_id("mistralai/Mistral-7B-v0.3")

    def show_report(self, model_index, rotors=27, layers=10):
        model = self.models[model_index]
        diff = self.calculate_difficulty(model['size_gb'])
        est_size = self.estimate_crystal_size(rotors, layers)

        print("\n" + "💎" * 20)
        print(f" CRYSTALLIZATION REPORT: {model['name']}")
        print(" " + "💎" * 20)
        print(f" - Target Model: {model['id']}")
        print(f" - Original Size: {model['size_gb']:.2f} GB")
        print(f" - Hardare Difficulty: {diff}")
        print(f" - Configuration: {rotors} Rotors, {layers} Layers")
        print(f" - Expected Sovereign Body Size: ~{est_size:.3f} MB")
        print(f" - Compression Ratio: ~{ (model['size_gb']*1024) / est_size :.1f}:1")
        print(f" - Recommendation: {model['recommendation']}")
        print("-" * 40)
        print("위상 로터를 가동할 준비가 되셨나요? (y/n)")

if __name__ == "__main__":
    selector = SovereignSelector()
    selector.list_models()

    # Example interaction
    # selector.show_report(0)
