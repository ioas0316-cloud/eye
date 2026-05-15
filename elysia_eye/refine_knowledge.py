import sys
import os
import json

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xray_projector import XRayProjector
from knowledge_refiner import KnowledgeRefiner
from archive_manager import SovereignArchive

def run_refinery():
    print("====================================================")
    print("   ELYSIA-EYE: KNOWLEDGE PURIFICATION SYSTEM")
    print("====================================================")
    print("Target Hardware: GTX 1060 3GB Optimization Active")
    print("----------------------------------------------------")

    prompt = input("정제할 지식이나 질문을 입력하세요 (예: 피타고라스의 정리): ")
    if not prompt:
        prompt = "Pythagorean theorem"

    print("\n[1/3] 엔진 가동 및 엑스레이 스캐닝 시작...")
    try:
        projector = XRayProjector()
        refiner = KnowledgeRefiner(projector)
        archive = SovereignArchive()

        print(f"\n[2/3] '{prompt}'에 대한 지능 정수 추출 중...")
        seed, p_rate = refiner.refine_to_seed(prompt)

        print("\n[3/3] 소버린 아카이브에 '지능의 씨앗' 저장 중...")
        metadata = {
            "prompt": prompt,
            "purification_rate": p_rate,
            "hardware": "GTX 1060 3GB Optimized"
        }

        # Save as a readable JSON for the user to see the "Seed"
        seed_path = f"elysia_eye/outputs/seed_{prompt.replace(' ', '_')}.json"
        with open(seed_path, 'w', encoding='utf-8') as f:
            json.dump({"metadata": metadata, "seed": seed}, f, indent=4, ensure_ascii=False)

        print("----------------------------------------------------")
        print("정제 완료!")
        print(f"지능 순도: {p_rate*100:.1f}% (불필요한 노이즈 {(1-p_rate)*100:.1f}% 제거됨)")
        print(f"추출된 씨앗: {seed_path}")
        print("이제 이 씨앗은 엘리시아 본체의 양분으로 사용될 수 있습니다.")
        print("====================================================")

    except Exception as e:
        print(f"\n[오류 발생] 정제 과정 중 문제가 발생했습니다: {e}")

if __name__ == "__main__":
    run_refinery()
