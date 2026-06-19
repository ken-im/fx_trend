# Streamlit 앱 전환 계획서

> 작성일: 2026-06-19  
> 개정일: 2026-06-19 (정적 HTML / GitHub Pages 배포 경로 완전 제거)  
> 목적: 정적 HTML + GitHub Pages 배포 구조를 **폐기**하고 Streamlit Community Cloud 앱으로 **완전 전환**

---

## 1. 현재 구조 vs 목표 구조

### 현재 구조 (폐기 대상)

```
[로컬 실행] main.py
    → FXDataCollector (데이터 수집)
    → FXAnalyzer      (이동평균 계산)
    → FXVisualizer    (Plotly 차트 생성)
    → docs/index.html (정적 HTML 파일 저장)
         ↓
[배포] GitHub Pages (/docs 폴더 서빙)   ← 이 경로 전체를 제거한다
```

**문제점:**
- 데이터가 HTML 생성 시점에 고정 (실시간 갱신 불가)
- 갱신하려면 로컬에서 `main.py` 실행 후 커밋·푸시 필요
- 746 KB 파일(`docs/index.html`)을 매번 커밋해야 함 (저장소 비대화)

### 목표 구조 (단일 배포 경로)

```
[Streamlit Community Cloud]   ← 유일한 배포 경로
    streamlit_app.py
        → FXDataCollector (앱 실행 시 실시간 데이터 수집)
        → FXAnalyzer      (이동평균 계산)
        → FXVisualizer    (Plotly 차트 생성)
        → st.plotly_chart (브라우저에 직접 렌더링)
```

**이점:**
- 앱을 열 때마다 최신 데이터 자동 반영
- `docs/index.html` 커밋 불필요 → 저장소 경량화
- `@st.cache_data` TTL로 API 호출 최소화 (1시간 캐시)
- Streamlit의 반응형 UI (사이드바, 선택박스) 활용

> **중요:** GitHub Pages와의 공존은 고려하지 않는다. 본 전환의 목표는 정적 HTML 배포
> 경로를 완전히 폐기하고 Streamlit을 단일 진입점으로 만드는 것이다. 관련 GitHub 정리
> 작업은 [6. GitHub 정리 작업](#6-github-정리-작업-필수)을 참조한다.

---

## 2. 변경 파일 목록

### 신규 생성 (3개)

| 파일 | 역할 |
|------|------|
| `streamlit_app.py` | Streamlit 앱 진입점 (main.py 대체) |
| `.streamlit/config.toml` | Bloomberg 터미널 스타일 다크 테마 설정 |
| `requirements.txt` | 루트 레벨 requirements (Streamlit Cloud가 자동 탐지) |

### 수정 (3개)

| 파일 | 변경 내용 |
|------|-----------|
| `backend/requirements.txt` | `streamlit>=1.32.0` 추가 |
| `README.md` | GitHub Pages / 정적 HTML 배포 관련 문구를 Streamlit 배포 내용으로 교체 |
| `docs/EXECUTION_PLAN.md` | Phase 6(GitHub Pages 배포) 섹션을 폐기 표시 또는 Streamlit 배포로 교체 |

### 삭제 (1개) — 필수

| 파일 | 처리 방안 |
|------|----------|
| `docs/index.html` | `git rm docs/index.html` 로 **추적 제거 후 커밋**. 이후 `.gitignore`로 재추적 방지. ([6장](#6-github-정리-작업-필수) 참조) |

### 변경 없음 (재활용)

| 파일 | 재활용 이유 |
|------|------------|
| `backend/config.py` | 통화 목록, MA 설정, 색상 그대로 사용 |
| `backend/src/data_collector.py` | `FXDataCollector` 클래스 그대로 사용 |
| `backend/src/analyzer.py` | `FXAnalyzer` 클래스 그대로 사용 |
| `frontend/src/visualizer.py` | `create_trend_chart()` 그대로 사용 |

### `main.py` 처리 방침

`main.py`는 **로컬 전용 HTML 생성 유틸리티로 격하**한다 (배포와 무관).

- 더 이상 배포 산출물을 만들지 않으며, 산출물(`docs/index.html`)은 `.gitignore`로 추적 제외된다.
- 인터넷 없는 환경에서 단발성 정적 리포트가 필요할 때를 위한 선택적 도구로만 남긴다.
- 혼란을 줄이기 위해 README의 "빠른 시작"은 `streamlit run`을 기본 경로로 안내하고,
  `main.py`는 "선택: 오프라인 정적 리포트 생성"으로 분리 표기한다.
- 유지가 불필요하다고 판단되면 후속 작업에서 `main.py`와 `frontend/src/visualizer.py`의
  HTML 생성 부분을 제거할 수 있다. (이번 전환 범위에서는 보존)

---

## 3. 신규 파일 상세 설계

### 3-1. `streamlit_app.py`

```
[앱 흐름]
1. st.set_page_config()         ← Bloomberg 스타일 페이지 설정
2. 헤더 렌더링                   ← st.markdown() (기존 HTML 헤더 재현)
3. 사이드바: 통화 선택            ← st.sidebar.selectbox()
4. @st.cache_data(ttl=3600)     ← 1시간 캐시
   load_fx_data(currency)
     → FXDataCollector.fetch_exchange_rate()
     → FXAnalyzer.calculate_moving_averages()
     → FXAnalyzer.get_statistics()
5. 통계 카드 렌더링              ← st.columns(3) + st.metric()
6. 차트 렌더링                   ← FXVisualizer.create_trend_chart()
                                   + st.plotly_chart(use_container_width=True)
7. 푸터 렌더링                   ← st.markdown()
```

**캐시 전략:**
- `@st.cache_data(ttl=3600)`: 통화별로 1시간 캐시
- 사용자가 통화를 전환해도 이미 로드된 데이터는 재사용

**에러 처리 (추가 반영):**
- 데이터 수집 실패(네트워크/소스 차단) 시 `st.error()`로 사용자 친화적 메시지 표시
- `try/except`로 감싸고, 실패 시 앱이 죽지 않도록 빈 상태 화면 제공
- 캐시 무효화를 위한 "새로고침" 버튼(`st.button` + `st.cache_data.clear()`) 선택 제공

**Bloomberg 스타일 유지 방법:**
- `.streamlit/config.toml`의 `[theme]` 섹션으로 배경/텍스트 색상 지정
- `st.markdown()` + `unsafe_allow_html=True`로 기존 stat 카드 HTML 재활용
- Plotly 차트는 기존 `FXVisualizer.create_trend_chart()` 반환값 그대로 사용

### 3-2. `.streamlit/config.toml`

```toml
[theme]
base = "dark"
backgroundColor = "#0a0e14"       # Bloomberg 배경 (기존 body 색상)
secondaryBackgroundColor = "#161b22"  # 카드/사이드바 배경
primaryColor = "#ff8c00"          # Bloomberg 오렌지 (기존 --bloomberg-orange)
textColor = "#e6edf3"             # Bloomberg 텍스트 (기존 --bloomberg-text)
font = "monospace"                # Consolas/Monaco 계열

[server]
headless = true
```

### 3-3. 루트 `requirements.txt`

Streamlit Community Cloud는 루트 디렉토리의 `requirements.txt`를 자동으로 읽음.

```
finance-datareader>=0.9.50
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.14.0
python-dateutil>=2.8.2
streamlit>=1.32.0
```

**의존성 중복 관리 방침 (추가 반영):**
루트 `requirements.txt`와 `backend/requirements.txt`가 분리되면 버전 드리프트 위험이 있다.
다음 중 하나를 택한다.
- **(권장)** 루트 `requirements.txt`를 단일 진실 소스(SSOT)로 삼고, `backend/requirements.txt`는
  최소화하거나 README에 "로컬 개발용은 루트 파일 사용"으로 안내.
- 또는 `backend/requirements.txt` 상단에 `-r ../requirements.txt`를 두어 루트를 참조.

### 3-4. Python 버전 고정 (추가 반영)

Streamlit Cloud는 앱 생성 시 Python 버전을 선택한다. 재현성을 위해 다음 중 하나로 고정한다.
- Streamlit Cloud "Advanced settings"에서 Python 3.11 명시, 또는
- 루트에 `runtime.txt` 추가:

```
python-3.11
```

---

## 4. Streamlit Community Cloud 배포 설정

### GitHub 연결 설정값

| 항목 | 값 |
|------|-----|
| Repository | `ken-im/fx_trend` |
| Branch | `main` |
| Main file path | `streamlit_app.py` |
| Python version | 3.11 (권장) |

### 자동 배포 트리거
- `main` 브랜치에 푸시 시 자동 재배포
- Streamlit Cloud가 앱 실행 시마다 최신 데이터 조회

### 배포 URL 관리
- 배포 완료 후 발급되는 `https://<app-name>.streamlit.app` URL을 확보한다.
- 이 URL을 README 상단 배지/링크와 GitHub 저장소 About(홈페이지)에 등록한다. ([6장](#6-github-정리-작업-필수))

---

## 5. 스타일 매핑: 기존 HTML → Streamlit

| 기존 HTML/CSS | Streamlit 대응 방식 |
|--------------|-------------------|
| `body { background: #0a0e14 }` | `config.toml [theme] backgroundColor` |
| `color: #ff8c00` (Bloomberg 오렌지) | `config.toml primaryColor` |
| 통화 선택 `<select>` | `st.sidebar.selectbox()` |
| 통계 카드 3개 (`stat-high/low/current`) | `st.columns(3)` + `st.metric()` 또는 기존 HTML 재사용 |
| Plotly `<div>` 임베드 | `st.plotly_chart(fig, use_container_width=True)` |
| 생성 일시 footer | `st.caption()` |

---

## 6. GitHub 정리 작업 (필수)

> 정적 HTML → GitHub Pages 배포 경로를 **완전히 제거**하기 위한 상세 작업 목록.
> Streamlit 앱이 로컬에서 정상 동작함을 확인한 **후** 진행한다.

### 6-1. GitHub Pages 비활성화 (웹 UI)

> 현재 저장소는 `gh-pages` 브랜치가 없고 `main` 브랜치만 존재하므로, Pages는
> **`main` 브랜치의 `/docs` 폴더 서빙** 방식으로 설정되어 있을 가능성이 높다.

1. GitHub 저장소 페이지 → **Settings** 탭 이동
2. 좌측 사이드바 → **Pages**
3. **Build and deployment → Source** 에서 현재 설정 확인
   - `Deploy from a branch` 로 되어 있고 Branch가 `main` / `/docs` 라면 →
     **Branch 드롭다운을 `None`으로 변경 후 Save** (Pages 비활성화)
   - `GitHub Actions` 로 되어 있다면 → 연결된 Pages 배포 워크플로를 비활성화/삭제 (6-4 참조)
4. 비활성화 후 기존 `https://ken-im.github.io/fx_trend/` 접속 시 404가 되는지 확인
5. (선택) Pages 관련 커스텀 도메인이 설정되어 있었다면 DNS/도메인 설정도 함께 정리

> `gh` CLI가 설치/인증되어 있다면 다음으로도 가능:
> `gh api -X DELETE repos/ken-im/fx_trend/pages` (현재 환경엔 `gh` 미설치 → 웹 UI 권장)

### 6-2. `docs/index.html` 제거 및 재추적 방지

저장소에서 정적 산출물을 제거하고, 이후 `main.py` 로컬 실행이 다시 커밋되지 않도록 한다.

```powershell
# 1) 추적 제거 (로컬 파일은 git rm --cached 사용 시 보존됨)
git rm docs/index.html
# (로컬에서도 완전히 삭제하려면 위 명령 그대로, 로컬 보존을 원하면)
# git rm --cached docs/index.html
```

`.gitignore`에 다음 항목 추가 (정적 산출물 재추적 방지):

```gitignore
# 정적 HTML 배포 폐기에 따라 로컬 생성 산출물 무시
docs/index.html
```

> `docs/` 폴더 자체는 문서(`PRD`, `EXECUTION_PLAN`, 본 계획서)를 위해 유지하며,
> 기존 `!docs/.gitkeep` 규칙도 그대로 둔다.

### 6-3. 문서 동기화 (README / EXECUTION_PLAN)

정적 HTML / GitHub Pages 언급을 제거하거나 Streamlit 기준으로 교체한다.

`README.md` 수정 항목:
- "주요 기능"의 `정적 HTML 생성: GitHub Pages 배포 가능` 문구 제거 →
  `웹 대시보드: Streamlit Community Cloud 배포` 로 교체
- "빠른 시작 → 실행": `python main.py` 대신 `streamlit run streamlit_app.py` 를 기본으로,
  `main.py`는 "선택: 오프라인 정적 리포트" 로 분리
- "프로젝트 구조": `docs/index.html # 생성된 대시보드 (GitHub Pages)` 줄 제거,
  `streamlit_app.py`, `.streamlit/config.toml`, 루트 `requirements.txt` 추가
- "기술 스택 → Deployment": `GitHub Pages` → `Streamlit Community Cloud`
- 상단에 배포 URL 배지/링크 추가 (예: `[![Open in Streamlit](...)](https://<app>.streamlit.app)`)

`docs/EXECUTION_PLAN.md` 수정 항목:
- **Phase 6: GitHub 배포 및 자동화** 의 GitHub Pages 설정/Actions(`update-dashboard.yml`) 내용을
  `~~취소선~~` 또는 "**[폐기] Streamlit Cloud 배포로 대체됨**" 표기로 정리하고,
  Streamlit 배포 절차(본 문서 4장 링크)로 대체
- 상단 "핵심 기술"·"목표"의 `GitHub Pages` 표현을 `Streamlit Community Cloud` 로 교체
- "배포 준비 체크리스트"의 GitHub Pages 항목 제거

### 6-4. GitHub Actions 워크플로 정리

- 현재 `.github/workflows` 폴더는 **존재하지 않으므로 삭제할 워크플로 없음**.
- 단, EXECUTION_PLAN에 예시로 적힌 `update-dashboard.yml`(HTML 자동 재생성+커밋)은
  **생성하지 않는다** (정적 HTML 경로 폐기와 모순).
- 향후 자동화가 필요하면 Streamlit Cloud 자동 재배포로 충분하며, 별도 Pages용 Actions는 두지 않는다.

### 6-5. 브랜치 점검

```powershell
git branch -a
git ls-remote --heads origin
```

- `gh-pages` 등 Pages 전용 브랜치가 보이면 삭제:

```powershell
git push origin --delete gh-pages   # 원격에 존재할 경우에만
git branch -D gh-pages              # 로컬에 존재할 경우에만
```

> 현재 확인 결과 원격은 `main`만 존재하므로 이 단계는 대개 No-op이다 (확인 목적).

### 6-6. 저장소 메타데이터(About) 갱신

GitHub 저장소 우측 **About** 영역:
- **Website** 필드: 기존 `https://ken-im.github.io/fx_trend/` (Pages URL) 제거 →
  Streamlit 앱 URL(`https://<app>.streamlit.app`)로 교체
- 설명(Description)에 "GitHub Pages" 문구가 있으면 "Streamlit dashboard" 등으로 수정
- Topics에 `streamlit` 추가, `github-pages` 가 있다면 제거

### 6-7. 보안: `secrets.toml` 무시 (추가 반영)

향후 Streamlit secrets 사용 가능성에 대비해 자격 증명이 커밋되지 않도록 `.gitignore`에 추가:

```gitignore
# Streamlit secrets (자격 증명 커밋 방지)
.streamlit/secrets.toml
```

> `.streamlit/config.toml`(테마)은 커밋 대상이며, `secrets.toml`만 무시한다.

### 6-8. 정리 작업 커밋

```powershell
git add .gitignore README.md docs/EXECUTION_PLAN.md docs/PLAN-streamlit-migration.md
git add streamlit_app.py .streamlit/config.toml requirements.txt backend/requirements.txt
git rm docs/index.html   # 6-2에서 미실행 시
git commit -m "chore: remove static HTML/GitHub Pages deployment, migrate to Streamlit"
git push origin main
```

---

## 7. 구현 순서 (단계별 작업)

### Step 1 — `.streamlit/config.toml` 생성
Bloomberg 다크 테마 적용. 앱 시각적 기반 구성.

### Step 2 — 루트 `requirements.txt` 생성
Streamlit Cloud가 의존성을 인식하도록 루트에 파일 생성. (+ 선택: `runtime.txt`)

### Step 3 — `streamlit_app.py` 작성
- 기존 `main.py` 로직을 Streamlit 구조로 재구성
- `FXDataCollector`, `FXAnalyzer`, `FXVisualizer` 그대로 import
- `@st.cache_data(ttl=3600)` 적용 + 데이터 수집 실패 시 `st.error()` 처리
- 통계 카드: 기존 `create_summary_html()` HTML을 `st.markdown(unsafe_allow_html=True)`로 렌더링하여 스타일 100% 보존

### Step 4 — `backend/requirements.txt` 업데이트
`streamlit>=1.32.0` 추가 (또는 3-3의 단일화 방침 적용).

### Step 5 — 로컬 검증
```powershell
streamlit run streamlit_app.py
```

### Step 6 — Streamlit Cloud 배포
```powershell
git add .
git commit -m "feat: add Streamlit app"
git push origin main
```
Streamlit Community Cloud 대시보드에서 앱 생성 및 배포 확인 → 앱 URL 확보.

### Step 7 — GitHub 정리 (6장 전체 실행)
Pages 비활성화 → `docs/index.html` 제거 → `.gitignore`/README/EXECUTION_PLAN 동기화 →
브랜치·About 점검 → 정리 커밋·푸시.

---

## 8. 고려사항 및 리스크

| 항목 | 내용 |
|------|------|
| **데이터 수집 시간** | FinanceDataReader로 4개 통화 × 8년 데이터 수집 시 초기 로딩 약 10~20초 예상. `@st.cache_data` TTL로 이후 로딩은 즉시. |
| **Streamlit Cloud 슬립** | 무료 플랜은 비활성 시 슬립 진입. 첫 방문 시 콜드 스타트 발생 가능. |
| **FinanceDataReader 제한** | 과도한 호출 시 차단 가능성. TTL 캐시로 최소화하고 실패 시 `st.error()` 처리. |
| **Pages 비활성화 영향** | 기존 `ken-im.github.io/fx_trend` URL은 폐기됨. 외부에 공유된 링크가 있다면 Streamlit URL로 안내 교체 필요. |
| **의존성 드리프트** | 루트/백엔드 requirements 이원화 시 버전 불일치 위험 → 3-3의 단일화 방침으로 완화. |
| **main.py 격하** | 정적 HTML은 로컬 전용 도구로만 남고 배포에는 사용하지 않음. 산출물은 gitignore 처리. |

---

## 9. 완료 기준 (Definition of Done)

### Streamlit 앱
- [ ] `streamlit_app.py` 로컬에서 정상 실행
- [ ] Bloomberg 다크 테마 적용 확인 (배경색 `#0a0e14`, 오렌지 강조색)
- [ ] 통화 선택 시 차트 및 통계 카드 교체 확인
- [ ] 이동평균 3개 (MA3M/MA1Y/MA3Y) 차트에 정상 표시
- [ ] 데이터 수집 실패 시 에러 메시지 정상 노출
- [ ] Streamlit Community Cloud 배포 URL 정상 접속
- [ ] 앱 로딩 후 최신 날짜 데이터 표시 확인

### GitHub 정리 (정적 HTML/Pages 제거)
- [ ] GitHub Pages 비활성화 (Settings → Pages → Source: None) 및 기존 URL 404 확인
- [ ] `docs/index.html` 추적 제거 및 커밋 완료
- [ ] `.gitignore`에 `docs/index.html`, `.streamlit/secrets.toml` 추가
- [ ] README의 GitHub Pages/정적 HTML 문구 제거 및 Streamlit 기준 갱신
- [ ] EXECUTION_PLAN의 Phase 6(GitHub Pages) 폐기 표기
- [ ] 저장소 About의 Website를 Streamlit URL로 교체, Topics 정리
- [ ] `gh-pages` 등 잔여 Pages 브랜치 없음 확인
