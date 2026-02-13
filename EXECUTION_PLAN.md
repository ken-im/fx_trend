# FX Trend Dashboard 실행 계획서

## 📋 프로젝트 개요

**목표**: Python 기반 환율 트렌드 분석 대시보드를 개발하고 GitHub Pages로 배포

**기간**: Phase 1-5 순차 진행

**핵심 기술**: Python, FinanceDataReader, Plotly, GitHub Pages

---

## 🏗 프로젝트 구조

```
fx_trend/
├── src/                          # 소스 코드 모듈
│   ├── __init__.py              # 패키지 초기화
│   ├── data_collector.py        # 데이터 수집 모듈
│   ├── analyzer.py              # 분석 모듈 (이동평균 등)
│   └── visualizer.py            # 시각화 모듈 (Plotly)
├── docs/                        # GitHub Pages 배포 디렉토리
│   └── index.html              # 생성된 대시보드
├── config.py                    # 설정 파일
├── main.py                      # 메인 실행 파일
├── requirements.txt             # 의존성 목록
├── README.md                    # 프로젝트 문서
├── PRD-fx_trend_dashboard.md   # 요구사항 정의서
└── EXECUTION_PLAN.md           # 본 실행 계획서
```

---

## 📅 Phase별 실행 계획

### ✅ Phase 1: 프로젝트 기본 구조 설정 [완료]

**목표**: 프로젝트 디렉토리 구조 및 기본 설정 파일 생성

**산출물**:
- [x] 디렉토리 구조 생성 (src/, docs/)
- [x] requirements.txt - Python 의존성 정의
- [x] .gitignore - Git 제외 파일 설정
- [x] README.md - 프로젝트 문서
- [x] config.py - 설정 관리

**다음 단계**: Phase 2로 진행

---

### 🔄 Phase 2: 데이터 수집 모듈 개발 [완료]

**목표**: FinanceDataReader를 이용한 환율 데이터 수집 기능 구현

**주요 기능**:
- [x] `FXDataCollector` 클래스 구현
- [x] 환율 데이터 수집 (`fetch_exchange_rate`)
- [x] 데이터 전처리 (결측치 처리, 날짜 정렬)
- [x] 다중 통화 지원 (`get_multiple_currencies`)

**파일**: `src/data_collector.py`

**검증 방법**:
```python
from src.data_collector import FXDataCollector

collector = FXDataCollector()
df = collector.fetch_exchange_rate('USD/KRW', period_years=5)
print(df.head())
print(df.info())
```

**다음 단계**: Phase 3로 진행

---

### 🔄 Phase 3: 분석 모듈 개발 [완료]

**목표**: 이동평균 계산 및 통계 분석 기능 구현

**주요 기능**:
- [x] `FXAnalyzer` 클래스 구현
- [x] 이동평균 계산
  - MA3M (60일)
  - MA1Y (250일)
  - MA3Y (750일)
- [x] 통계 정보 계산 (최고/최저/현재 환율)
- [x] 변동률 계산 (일별, 누적)

**파일**: `src/analyzer.py`

**검증 방법**:
```python
from src.analyzer import FXAnalyzer

analyzer = FXAnalyzer()
ma_periods = {'MA3M': 60, 'MA1Y': 250, 'MA3Y': 750}
df_analyzed = analyzer.analyze_trend(df, ma_periods)
statistics = analyzer.get_statistics(df_analyzed)
print(statistics)
```

**다음 단계**: Phase 4로 진행

---

### 🔄 Phase 4: 시각화 모듈 개발 [완료]

**목표**: Plotly를 이용한 인터랙티브 그래프 생성 및 HTML 출력

**주요 기능**:
- [x] `FXVisualizer` 클래스 구현
- [x] 환율 트렌드 차트 생성
  - 원본 환율 데이터
  - 이동평균선 (MA3M, MA1Y, MA3Y)
  - 최고/최저/현재 환율 마커
  - 현재 날짜 수직선
- [x] 요약 정보 HTML 생성
- [x] 완전한 HTML 파일 생성 (CSS 포함)

**파일**: `src/visualizer.py`

**그래프 요구사항**:
- X축: 날짜 (3개월 간격 표시)
- Y축: 환율 (KRW)
- 반응형 디자인
- 인터랙티브 호버 정보

**다음 단계**: Phase 5로 진행

---

### 🔄 Phase 5: 통합 및 배포 준비 [완료]

**목표**: 전체 파이프라인 통합 및 GitHub Pages 배포 준비

**주요 작업**:
- [x] `main.py` - 전체 프로세스 통합
- [x] HTML 생성 자동화
- [x] docs/index.html 출력

**실행 방법**:
```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 대시보드 생성
python main.py

# 4. 결과 확인
# docs/index.html 파일을 브라우저로 열기
```

**다음 단계**: Phase 6로 진행

---

### 🔜 Phase 6: GitHub 배포 및 자동화 [예정]

**목표**: GitHub Pages 배포 및 자동 업데이트 설정

**주요 작업**:
- [ ] Git 저장소 초기화
- [ ] GitHub Repository 생성
- [ ] GitHub Pages 설정
  - Settings > Pages > Source: main branch, /docs folder
- [ ] (선택) GitHub Actions 자동화
  - 주기적 데이터 업데이트
  - HTML 자동 재생성

**GitHub Actions 예시** (선택):
```yaml
# .github/workflows/update-dashboard.yml
name: Update FX Dashboard

on:
  schedule:
    - cron: '0 0 * * *'  # 매일 자정
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Generate dashboard
        run: python main.py
      - name: Commit and push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/index.html
          git commit -m "Update dashboard" || exit 0
          git push
```

**배포 후 확인**:
- URL: `https://[username].github.io/fx_trend/`

**다음 단계**: Phase 7로 진행

---

### 🔜 Phase 7: 기능 확장 [예정]

**목표**: 추가 기능 구현 및 사용성 개선

**우선순위 1**:
- [ ] 다중 통화 선택 UI
  - 드롭다운으로 USD/JPY/EUR 선택
  - JavaScript로 동적 그래프 전환
- [ ] 기간 선택 기능
  - 1년, 3년, 5년, 전체 기간
- [ ] 이동평균선 On/Off 토글

**우선순위 2**:
- [ ] 반응형 디자인 개선 (모바일)
- [ ] 다크 모드 지원
- [ ] 데이터 다운로드 기능 (CSV)

**우선순위 3**:
- [ ] 추가 기술지표
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
- [ ] 환율 예측 기능 (선택)
- [ ] 알림 기능 (이메일/웹훅)

---

## 🎯 현재 진행 상황

### 완료된 작업 ✅
1. ✅ 프로젝트 구조 설계 및 생성
2. ✅ 의존성 관리 (requirements.txt)
3. ✅ 데이터 수집 모듈 (data_collector.py)
4. ✅ 분석 모듈 (analyzer.py)
5. ✅ 시각화 모듈 (visualizer.py)
6. ✅ 메인 실행 파일 (main.py)
7. ✅ 설정 파일 (config.py)
8. ✅ 문서화 (README.md, PRD)

### 다음 단계 🔜
1. **즉시 실행 가능**: 환경 설정 및 첫 실행
2. **단기**: GitHub 배포
3. **중기**: 다중 통화 UI 개선
4. **장기**: 추가 기술지표 및 예측 기능

---

## 🚀 빠른 시작 가이드

### 1단계: 환경 설정
```powershell
# PowerShell에서 실행

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt
```

### 2단계: 대시보드 생성
```powershell
# 메인 스크립트 실행
python main.py
```

### 3단계: 결과 확인
```powershell
# 생성된 HTML 파일 열기
start docs\index.html
```

### 4단계: Git 초기화 (선택)
```powershell
git init
git add .
git commit -m "Initial commit: FX Trend Dashboard"
git branch -M main
git remote add origin https://github.com/[username]/fx_trend.git
git push -u origin main
```

---

## 📊 예상 결과물

### 대시보드 기능
1. **헤더 영역**
   - 프로젝트 제목
   - 간단한 설명

2. **요약 카드**
   - 최고 환율 (날짜 포함)
   - 최저 환율 (날짜 포함)
   - 현재 환율 (날짜 포함)

3. **메인 그래프**
   - 환율 원본 데이터 (실선)
   - MA3M (60일, 점선)
   - MA1Y (250일, 점선)
   - MA3Y (750일, 점선)
   - 최고점 마커 (빨강)
   - 최저점 마커 (파랑)
   - 현재 날짜 수직선 (초록)

4. **푸터**
   - 데이터 출처
   - 생성 일시
   - 저작권 정보

---

## ⚙️ 설정 커스터마이징

### config.py 주요 설정

**통화 추가**:
```python
CURRENCIES = {
    'CNY/KRW': {  # 중국 위안화 추가
        'symbol': 'CNY/KRW',
        'name': '중국 위안화',
        'fdr_code': 'CNY/KRW'
    }
}
```

**이동평균 기간 변경**:
```python
MOVING_AVERAGES = {
    'MA1M': {'days': 20, 'label': '1개월', 'color': '#FF6B6B'},
    'MA6M': {'days': 120, 'label': '6개월', 'color': '#4ECDC4'}
}
```

**그래프 크기 조정**:
```python
GRAPH_CONFIG = {
    'width': 1600,  # 기본: 1200
    'height': 800,  # 기본: 600
}
```

---

## 🐛 문제 해결

### 일반적인 이슈

**1. FinanceDataReader 설치 오류**
```powershell
# 최신 버전으로 업데이트
pip install --upgrade finance-datareader
```

**2. 데이터 수집 실패**
- 인터넷 연결 확인
- FinanceDataReader 서버 상태 확인
- 통화 코드 확인

**3. HTML 생성 안됨**
- docs 폴더 존재 확인
- 쓰기 권한 확인

**4. 그래프가 표시되지 않음**
- Plotly CDN 연결 확인
- 브라우저 콘솔 에러 확인

---

## 📝 체크리스트

### 개발 완료 체크리스트
- [x] 프로젝트 구조 생성
- [x] 데이터 수집 모듈
- [x] 분석 모듈
- [x] 시각화 모듈
- [x] 메인 통합
- [x] 문서화

### 배포 준비 체크리스트
- [ ] 로컬 테스트 완료
- [ ] Git 저장소 초기화
- [ ] GitHub Repository 생성
- [ ] GitHub Pages 설정
- [ ] README 업데이트
- [ ] 스크린샷 추가

### 품질 보증 체크리스트
- [ ] 코드 주석 완성도
- [ ] 에러 처리 검증
- [ ] 다양한 기간 테스트
- [ ] 다양한 통화 테스트
- [ ] 반응형 디자인 확인
- [ ] 브라우저 호환성 확인

---

## 📚 참고 자료

- [FinanceDataReader 문서](https://github.com/FinanceData/FinanceDataReader)
- [Plotly Python 문서](https://plotly.com/python/)
- [GitHub Pages 가이드](https://pages.github.com/)
- [Pandas 문서](https://pandas.pydata.org/docs/)

---

## 👥 기여 및 피드백

프로젝트 개선 아이디어나 버그 리포트는 GitHub Issues를 통해 제출해주세요.

---

**작성일**: 2026-02-13  
**버전**: 1.0  
**상태**: Phase 1-5 완료, Phase 6-7 예정
