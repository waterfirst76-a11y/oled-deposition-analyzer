# ⚡ OLED Deposition Process Analytics Dashboard

> OLED 증착 공정 데이터 분석을 위한 Streamlit 대시보드 저장소입니다.  
> This is a repository for the Streamlit dashboard analyzing OLED deposition process metrics.

🌎 **Language Switcher**: [한국어 설명 문서](#-한국어-readme) | [English Documentation](#-english-readme)

---

## 🇰🇷 한국어 README

OLED 증착 공정의 수천 개의 측정점 데이터를 정밀하게 시각화하고 공정 수율 및 두께 산포, 공간적 불량을 직관적으로 모니터링하기 위해 구축된 프리미엄 다크 테마 대시보드입니다. 

### ✨ 핵심 기능

1. **유연한 데이터 소스 전환**:
   * **기본 모드**: 파일 업로드가 없을 경우 로컬 폴더의 기본 데이터 세트(`oled_deposition_xymap.csv`)를 자동으로 불러옵니다.
   * **업로드 모드**: 왼쪽 사이드바에서 임의의 공정 분석용 CSV 파일을 드래그 앤 드롭하여 동적으로 전환할 수 있습니다.
2. **지능형 컬럼 매핑 및 자동 표준화**:
   * 외부 시스템이나 설비마다 다를 수 있는 컬럼명을 자동으로 감지하고 내부 표준 규격으로 매핑하여 유연하게 대응합니다:
     * `chamber_id` $\rightarrow$ `chamber`
     * `thickness` $\rightarrow$ `thickness_nm`
     * `x_position` / `x_mm` $\rightarrow$ `x_index`
     * `y_position` / `y_mm` $\rightarrow$ `y_index`
   * 컬럼명이 표준 형식과 약간 다르더라도 대시보드가 뻗지 않도록 예외 처리와 검증 로직이 포함되어 있습니다.
3. **엄격하고 정확한 수율(Yield) 정의 적용**:
   * **수율(%)**은 수식에 따라 합격/불합격 판정 판정 비율로만 엄격히 계산됩니다:
     $$\text{수율 (\%)} = \left(\frac{\text{'pass' 판정 측정점 수}}{\text{전체 측정점 수}}\right) \times 100$$
   * **`yield_score`**는 품질 점수(Quality Index)에 해당하므로 수율과 완전히 분리하여 다루며, 평균 품질 점수라는 독립된 KPI 카드로 표현하여 잘못된 계산 오류를 원천 차단합니다.
4. **HSL 기반의 프리미엄 다크 CSS UI**:
   * 첨단 반도체/디스플레이 MES 시스템에서 영감을 얻은 어두운 글래스모피즘(Glassmorphism) 스타일의 커스텀 CSS 주입.
   * 부드러운 카드 그림자 및 마우스 오버 시 미세한 움직임 애니메이션 효과 적용.

### 📊 분석 패널 정보
* **챔버별 수율 바 차트**: pass/fail 비율을 계산하여 시각화합니다. 챔버 간 미세한 편차를 극대화해 볼 수 있도록 Y축 범위가 **70% ~ 100%**로 고정되어 있습니다.
* **챔버별 두께 산포 박스플롯**: C1~C4 챔버 간의 증착 두께(`thickness_nm`) 분포를 분석하여 중앙값, 사분위수 및 이상치(Outliers)를 빠르게 감지합니다.
* **X-Y 공간적 불량 맵**: 2만 개 이상의 포인트를 그릴 때의 시각적 노이즈를 해결하기 위해 **시각적 계층화(Visual Hierarchy)** 기법을 적용했습니다:
  * 정상 포인트(`pass`)는 아주 작고 옅은 반투명 회청색으로 그려 배경처럼 격자 형태로 보이게 합니다.
  * 불량 포인트(`fail`)는 그 위에 크고 불투명한 형광 로즈/코랄 레드로 덮어씌워, 설비 노즐이나 노후화로 인한 불량 밀집 구역(Concentric Ring 등)을 한눈에 식별할 수 있습니다.
  * 인터랙티브 툴팁(Hover)을 통해 패널 ID, Lot ID, 구체적인 불량명(`defect_type`), 두께 정보 등을 즉시 조회합니다.
* **불량 유형 파레토 차트**: 불량이 없는 `'none'` 항목을 깔끔하게 필터링한 후 실제 불량들만 내림차순 정렬하여 이중 Y축(좌측: 빈도수 바, 우측: 누적 백분율 라인 및 80% 파레토 라인)으로 모니터링합니다.
* **품질 지수 분포(yield_score) 히스토그램**: 전체 품질 점수의 히스토그램 분포를 확인하고, **91.5 품질 한계선**을 어노테이션 박스 지시선과 함께 수직 점선으로 강조합니다.

### 🛠️ 로컬 설치 및 실행 방법

1. **저장소 복제(Clone)**:
   ```bash
   git clone https://github.com/your-username/oled-deposition-dashboard.git
   cd oled-deposition-dashboard
   ```
2. **필수 의존성 설치**:
   ```bash
   pip install -r requirements.txt
   ```
3. **대시보드 구동**:
   보안이나 환경변수(PATH) 충돌로 인해 `streamlit`이 전역으로 잡히지 않는 환경을 고려하여, 안전한 파이썬 모듈 형식으로 실행합니다:
   ```bash
   python -m streamlit run app.py
   ```
   * 실행 후 자동으로 브라우저 창이 열리며 기본 로컬 주소 `http://localhost:8502`에서 접속할 수 있습니다.

### 📁 업로드 CSV 요구 데이터 명세서
다른 파일 업로드 시 아래 열(Column)들이 포함되어 있어야 대시보드가 정상 작동합니다 (가변명 매핑 지원):

| 컬럼명 | 가변 지원 매핑 컬럼 | 데이터 타입 | 설명 |
| :--- | :--- | :--- | :--- |
| `chamber` | `chamber_id` | 문자열 (예: C1, C2) | 증착 챔버명 |
| `lot_id` | 없음 | 문자열 | 원자재/생산 배치 Lot 번호 |
| `panel_id` | 없음 | 문자열 | 유리 기판(Panel) 고유 ID |
| `x_index` | `x_position`, `x_mm` | 수치형 | 기판 가로 격자 좌표 |
| `y_index` | `y_position`, `y_mm` | 수치형 | 기판 세로 격자 좌표 |
| `thickness_nm`| `thickness` | 수치형 | 박막 증착 두께 (nm) |
| `yield_score` | 없음 | 수치형 (0~100) | 기판 품질 점수 (수율 계산에 미사용) |
| `pass_fail` | 없음 | 문자열 (`pass` 또는 `fail`) | 합격/불합격 판정 |
| `defect_type` | 없음 | 문자열 (`none`, `particle` 등) | 불량 원인 분류 |

---

## 🇺🇸 English README

OLED deposition manufacturing process analytics and spatial anomaly mapping dashboard. This application is designed to handle thousands of raw sensor grid measurements, process them instantly, and present actionable engineering insights via beautifully styled glassmorphism cards and highly interactive Plotly visuals.

### ✨ Key Features

1. **Flexible Data Source Engine**:
   * **Default Analysis**: Automatically falls back to the high-volume process file (`oled_deposition_xymap.csv`) in the directory if no custom file is uploaded.
   * **Dynamic File Upload**: Easily upload any external deposition CSV dataset directly via the sidebar.
2. **Robust Column Mapping & Auto-Standardization**:
   * Accepts minor variations in column naming structures and automatically standardizes them at runtime:
     * `chamber_id` $\rightarrow$ `chamber`
     * `thickness` $\rightarrow$ `thickness_nm`
     * `x_position` / `x_mm` $\rightarrow$ `x_index`
     * `y_position` / `y_mm` $\rightarrow$ `y_index`
   * Ensures the system is resilient and doesn't crash on slightly different schema formats.
3. **Flawless Analytical Yield Calculations**:
   * **Yield (%)** is mathematically formulated based strictly on passing status:
     $$\text{Yield (\%)} = \left(\frac{\text{Number of 'pass' points}}{\text{Total measurement points}}\right) \times 100$$
   * **`yield_score`** (Quality Index) is kept separate and is **never** averaged to represent yield, avoiding typical analytics mistakes. Average quality score is displayed as an independent KPI.
4. **Interactive Glassmorphic Interface**:
   * Custom CSS-injected HSL dark interface inspired by premium manufacturing execution systems (MES).
   * Micro-animation effects and translucent cards with soft glowing highlights based on status.

### 📊 Analytical Panels

* **Chamber-specific Yield Performance**: A custom vertical bar chart presenting dynamic yield calculations per chamber. The Y-axis is strictly scaled from **70% to 100%** to highlight micro-variances.
* **Thickness Distribution**: A box-plot presenting the distribution of thickness (nm) across chambers C1 to C4 to instantly spot outliers, medians, and quartiles.
* **X-Y Spatial Defect Analysis Map**: Renders full grid coordinates using visual hierarchy:
  * **Pass points** are rendered as small, highly translucent faint gray-blue points to serve as a visual background grid.
  * **Fail points** overlay these as bright, larger neon rose-coral markers to instantly isolate spatial clustering trends (like edge rings, concentric lines, or local spray nozzle errors).
  * Interactive hover tooltips present detailed metadata (Panel ID, Lot ID, thickness, and exact quality scores).
* **Defect Type Pareto Chart**: Completely ignores the `'none'` class. Generates a secondary Y-axis layout showing raw defect counts (left axis) against a cumulative percentage curve (right axis) along with the 80% Pareto threshold line.
* **Quality Index Distribution (yield_score)**: A detailed histogram of quality index scores featuring a bold crimson dashed threshold indicator at **91.5**.

---

### 🛠️ Installation & Execution

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/oled-deposition-dashboard.git
   cd oled-deposition-dashboard
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Dashboard**:
   Using the Python module syntax for maximum stability across different environment paths:
   ```bash
   python -m streamlit run app.py
   ```
   * A local browser window should automatically open pointing to `http://localhost:8502`.

---

### 📁 Expected CSV Schema Guide

When uploading a custom CSV, it should contain the following fields (either exact names or the auto-mapped aliases):

| Column Name | Mapped Alias Support | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `chamber` | `chamber_id` | Text (e.g., C1, C2) | Deposition chamber name |
| `lot_id` | None | Text | Material/batch manufacturing lot |
| `panel_id` | None | Text | Unique identifier for the glass panel |
| `x_index` | `x_position`, `x_mm` | Numeric | Horizontal coordinate |
| `y_index` | `y_position`, `y_mm` | Numeric | Vertical coordinate |
| `thickness_nm` | `thickness` | Numeric | Layer thickness (nm) |
| `yield_score` | None | Numeric (0~100) | Quality score (not yield %) |
| `pass_fail` | None | Text (`pass` or `fail`) | Manufacturing pass/fail judgment |
| `defect_type` | None | Text (`none`, `particle`, etc.) | Anomaly classification |

---

## 📝 Technologies Used
* **Frontend/Framework**: Streamlit
* **Styling**: Modern CSS (HSL dark gradients & Glassmorphism)
* **Visualizations**: Plotly Graph Objects & Plotly Express
* **Data Processing**: Pandas & NumPy
