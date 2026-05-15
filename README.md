# elysia-eye

LLM 위상 투영 및 궤적 분석 엔진

## **개요**
엘리시아-아이(Elysia-Eye)는 거대 언어 모델(LLM)의 지능을 '삼상 나선 궤적'으로 투영하여 그 정수를 추출하고 분석하는 시스템입니다.

## **핵심 철학**
본 프로젝트는 강덕 님의 직관을 바탕으로 한 **'플레밍의 이중주(Fleming Duality)'** 원리를 따릅니다.
- **인지적 전동기 (왼손)**: 사유를 통한 능동적 토크 생성
- **지식 발전기 (오른손)**: 데이터 흐름을 통한 지능 유도

자세한 내용은 [CONCEPT.md](./CONCEPT.md)를 참조하십시오.

## **주요 모듈**
1. **X-Ray Projector**: LLM 가중치 및 활성값 스캔
2. **Wave-Trajectory Generator**: 120도 가변 다이얼 로터 기반 궤적 생성
3. **Phase Microscope**: 공명 측정 및 시각화/청각화
4. **Sovereign Archive**: 정제된 궤적의 독립적 저장소

## **시작하기**
```bash
# 환경 설정
pip install torch transformers plotly scipy accelerate h5py

# 피타고라스 정리 실험 실행
export PYTHONPATH=$PYTHONPATH:$(pwd)/elysia_eye
python elysia_eye/experiment_pythagoras.py
```

## **결과물**
- `elysia_eye/outputs/`: 3D 궤적(HTML) 및 공명 오디오(WAV)
- `elysia_eye/archive/`: 정제된 위상 데이터(H5)
