# FX Trend Dashboard

환율 트렌드 및 이동평균 분석 대시보드

## 📊 프로젝트 개요

주요 통화(USD, JPY, EUR 등)의 환율 데이터를 수집하고, 환율 추세 및 이동평균(Moving Average) 지표를 시각화하여 환율 변동 흐름을 직관적으로 파악할 수 있는 대시보드입니다.

## 🎯 주요 기능

- **환율 데이터 수집**: FinanceDataReader를 활용한 실시간 환율 데이터 수집
- **이동평균 분석**: 
  - 3개월 이동평균 (MA3M: 60일)
  - 1년 이동평균 (MA1Y: 250일)
  - 3년 이동평균 (MA3Y: 750일)
- **시각화**: Plotly를 이용한 인터랙티브 그래프
- **정적 HTML 생성**: GitHub Pages 배포 가능

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 실행

```bash
# 대시보드 생성
python main.py

# 생성된 HTML 파일 확인
# docs/index.html
```

## 📁 프로젝트 구조

```
fx_trend/
├── src/
│   ├── data_collector.py    # 데이터 수집 모듈
│   ├── analyzer.py           # 분석 모듈
│   └── visualizer.py         # 시각화 모듈
├── docs/
│   └── index.html            # 생성된 대시보드 (GitHub Pages)
├── main.py                   # 메인 실행 파일
├── requirements.txt          # 의존성 목록
└── README.md
```

## 🛠 기술 스택

- **Language**: Python 3.x
- **Data Source**: FinanceDataReader
- **Data Processing**: pandas, numpy
- **Visualization**: Plotly
- **Deployment**: GitHub Pages

## 📈 지원 통화

- USD/KRW (미국 달러)
- JPY/KRW (일본 엔화)
- EUR/KRW (유로화)

## 📄 라이선스

MIT License

## 👤 작성자

Your Name
