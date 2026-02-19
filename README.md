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
pip install -r backend/requirements.txt
```

또는 Windows PowerShell에서 자동 설치:
```powershell
.\setup.ps1
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
├── backend/                  # 데이터 생성 및 관리
│   ├── src/
│   │   ├── data_collector.py    # 환율 데이터 수집
│   │   └── analyzer.py           # 이동평균 계산 및 통계 분석
│   ├── config.py             # 통화 설정, 이동평균 설정
│   └── requirements.txt      # Python 의존성
│
├── frontend/                 # 화면 표현 및 관리
│   └── src/
│       └── visualizer.py     # Plotly 그래프 생성 및 HTML 생성
│
├── docs/                     # 문서 및 배포
│   ├── PRD-fx_trend_dashboard.md      # 요구사항 정의서
│   ├── EXECUTION_PLAN.md              # 실행 계획
│   └── index.html                     # 생성된 대시보드 (GitHub Pages)
│
├── main.py                   # 전체 실행 스크립트
├── setup.ps1                 # Windows 자동 설치 스크립트
├── README.md                 # 프로젝트 문서
├── .gitignore
└── LICENSE
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
- USD/BRL (브라질 헤알, USD 기준)

드롭다운 메뉴에서 통화를 선택하여 각 통화의 환율 트렌드를 확인할 수 있습니다.

## 📄 라이선스

MIT License

## 👤 작성자

Your Name
