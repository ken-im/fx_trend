# FX Trend Dashboard 설치 스크립트 (PowerShell)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "FX Trend Dashboard 설치 시작" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 1. Python 버전 확인
Write-Host "[1/4] Python 버전 확인 중..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python이 설치되어 있지 않습니다." -ForegroundColor Red
    Write-Host "  Python 3.8 이상을 설치해주세요: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 2. 가상환경 생성
Write-Host "[2/4] 가상환경 생성 중..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "! 가상환경이 이미 존재합니다. 기존 환경을 사용합니다." -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 가상환경 생성 완료" -ForegroundColor Green
    } else {
        Write-Host "✗ 가상환경 생성 실패" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# 3. 가상환경 활성화
Write-Host "[3/4] 가상환경 활성화 중..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 가상환경 활성화 완료" -ForegroundColor Green
} else {
    Write-Host "✗ 가상환경 활성화 실패" -ForegroundColor Red
    Write-Host "  PowerShell 실행 정책을 확인해주세요." -ForegroundColor Red
    Write-Host "  관리자 권한으로 실행: Set-ExecutionPolicy RemoteSigned" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# 4. 의존성 설치
Write-Host "[4/4] 의존성 설치 중..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 의존성 설치 완료" -ForegroundColor Green
} else {
    Write-Host "✗ 의존성 설치 실패" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "================================" -ForegroundColor Cyan
Write-Host "✓ 설치 완료!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "다음 명령으로 대시보드를 생성하세요:" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
