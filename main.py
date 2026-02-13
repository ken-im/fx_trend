"""
FX Trend Dashboard 메인 실행 파일
"""

import os
import sys
from pathlib import Path

# Windows 콘솔 UTF-8 인코딩 설정
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.data_collector import FXDataCollector
from src.analyzer import FXAnalyzer
from src.visualizer import FXVisualizer
import config


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("FX Trend Dashboard 생성 시작")
    print("=" * 60)
    
    # 1. 데이터 수집
    print("\n[1/4] 데이터 수집 중...")
    collector = FXDataCollector()
    
    currency_code = config.DEFAULT_CURRENCY
    currency_info = config.CURRENCIES[currency_code]
    
    # 이동평균 계산을 위해 표시 기간 + warmup 기간만큼 수집
    total_period_years = config.DEFAULT_PERIOD_YEARS + config.MA_WARMUP_YEARS
    
    try:
        df_all = collector.fetch_exchange_rate(
            currency_code=currency_info['fdr_code'],
            period_years=total_period_years
        )
        print(f"✓ {currency_info['name']} 데이터 수집 완료 ({len(df_all)}개 레코드)")
        print(f"  - 수집 기간: {total_period_years}년 (표시: {config.DEFAULT_PERIOD_YEARS}년 + 이동평균 계산용: {config.MA_WARMUP_YEARS}년)")
    except Exception as e:
        print(f"✗ 데이터 수집 실패: {str(e)}")
        return
    
    # 2. 데이터 분석
    print("\n[2/4] 데이터 분석 중...")
    analyzer = FXAnalyzer()
    
    # 이동평균 기간 추출
    ma_periods = {name: info['days'] for name, info in config.MOVING_AVERAGES.items()}
    
    try:
        # 전체 데이터로 이동평균 계산 (warmup 기간 포함)
        df_analyzed_all = analyzer.analyze_trend(df_all, ma_periods)
        print("✓ 이동평균 계산 완료 (전체 기간)")
        print(f"  - MA3M (60일), MA1Y (250일), MA3Y (750일)")
        
        # 표시용 데이터: 최근 지정 기간만 추출
        from datetime import timedelta
        cutoff_date = df_analyzed_all['Date'].max() - timedelta(days=config.DEFAULT_PERIOD_YEARS * 365)
        df_display = df_analyzed_all[df_analyzed_all['Date'] >= cutoff_date].copy()
        print(f"✓ 표시 기간 데이터 추출 완료 ({len(df_display)}개 레코드)")
        
        # 통계 분석 (표시 기간 데이터만)
        statistics = analyzer.get_statistics(df_display)
        print(f"✓ 통계 분석 완료")
        print(f"  - 최고: {statistics['max']['price']:,.2f}원 ({statistics['max']['formatted_date']})")
        print(f"  - 최저: {statistics['min']['price']:,.2f}원 ({statistics['min']['formatted_date']})")
        print(f"  - 현재: {statistics['current']['price']:,.2f}원 ({statistics['current']['formatted_date']})")
    except Exception as e:
        import traceback
        print(f"✗ 데이터 분석 실패: {str(e)}")
        traceback.print_exc()
        return
    
    # 3. 시각화
    print("\n[3/4] 그래프 생성 중...")
    visualizer = FXVisualizer(config.GRAPH_CONFIG)
    
    try:
        fig = visualizer.create_trend_chart(
            df=df_display,  # 표시 기간 데이터 사용
            currency_name=currency_info['name'],
            currency_symbol=currency_info['symbol'],  # 통화 심볼 추가
            ma_config=config.MOVING_AVERAGES,
            statistics=statistics
        )
        print("✓ 그래프 생성 완료")
        
        summary_html = visualizer.create_summary_html(
            statistics=statistics,
            currency_name=currency_info['name']
        )
        print("✓ 요약 정보 생성 완료")
    except Exception as e:
        import traceback
        print(f"✗ 시각화 실패: {str(e)}")
        print("\n상세 오류:")
        traceback.print_exc()
        return
    
    # 4. HTML 파일 저장
    print("\n[4/4] HTML 파일 저장 중...")
    
    # 출력 디렉토리 생성
    output_dir = Path(config.OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / config.OUTPUT_FILENAME
    
    try:
        visualizer.save_to_html(
            fig=fig,
            summary_html=summary_html,
            output_path=str(output_path),
            title="FX Trend Dashboard"
        )
        print(f"✓ HTML 파일 저장 완료: {output_path}")
    except Exception as e:
        print(f"✗ HTML 저장 실패: {str(e)}")
        return
    
    print("\n" + "=" * 60)
    print("✓ FX Trend Dashboard 생성 완료!")
    print("=" * 60)
    print(f"\n생성된 파일: {output_path}")
    print(f"브라우저에서 열어 확인하세요.")


if __name__ == '__main__':
    main()
