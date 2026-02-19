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

from backend.src.data_collector import FXDataCollector
from backend.src.analyzer import FXAnalyzer
from frontend.src.visualizer import FXVisualizer
import backend.config as config


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("FX Trend Dashboard 생성 시작")
    print("=" * 60)
    
    # 1. 모든 통화 데이터 수집
    print("\n[1/4] 데이터 수집 중...")
    collector = FXDataCollector()
    
    # 이동평균 계산을 위해 표시 기간 + warmup 기간만큼 수집
    total_period_years = config.DEFAULT_PERIOD_YEARS + config.MA_WARMUP_YEARS
    
    all_currency_data = {}
    
    for currency_code, currency_info in config.CURRENCIES.items():
        try:
            print(f"  - {currency_info['name']} 수집 중...")
            df_all = collector.fetch_exchange_rate(
                currency_code=currency_info['fdr_code'],
                period_years=total_period_years
            )
            all_currency_data[currency_code] = {
                'df': df_all,
                'info': currency_info
            }
            print(f"    ✓ {currency_info['name']} 데이터 수집 완료 ({len(df_all)}개 레코드)")
        except Exception as e:
            print(f"    ✗ {currency_info['name']} 수집 실패: {str(e)}")
            continue
    
    if not all_currency_data:
        print("\n✗ 수집된 데이터가 없습니다.")
        return
    
    print(f"\n✓ 총 {len(all_currency_data)}개 통화 데이터 수집 완료")
    print(f"  - 수집 기간: {total_period_years}년 (표시: {config.DEFAULT_PERIOD_YEARS}년 + 이동평균 계산용: {config.MA_WARMUP_YEARS}년)")
    
    # 2. 모든 통화 데이터 분석
    print("\n[2/4] 데이터 분석 중...")
    analyzer = FXAnalyzer()
    
    # 이동평균 기간 추출
    ma_periods = {name: info['days'] for name, info in config.MOVING_AVERAGES.items()}
    
    from datetime import timedelta
    analyzed_data = {}
    
    for currency_code, data in all_currency_data.items():
        try:
            print(f"  - {data['info']['name']} 분석 중...")
            df_all = data['df']
            
            # 전체 데이터로 이동평균 계산 (warmup 기간 포함)
            df_analyzed_all = analyzer.analyze_trend(df_all, ma_periods)
            
            # 표시용 데이터: 최근 지정 기간만 추출
            cutoff_date = df_analyzed_all['Date'].max() - timedelta(days=config.DEFAULT_PERIOD_YEARS * 365)
            df_display = df_analyzed_all[df_analyzed_all['Date'] >= cutoff_date].copy()
            
            # 통계 분석 (표시 기간 데이터만)
            statistics = analyzer.get_statistics(df_display)
            
            analyzed_data[currency_code] = {
                'df': df_display,
                'statistics': statistics,
                'info': data['info']
            }
            
            print(f"    ✓ 분석 완료 - 최고: {statistics['max']['price']:,.2f}원, 최저: {statistics['min']['price']:,.2f}원")
            
        except Exception as e:
            print(f"    ✗ {data['info']['name']} 분석 실패: {str(e)}")
            continue
    
    if not analyzed_data:
        print("\n✗ 분석된 데이터가 없습니다.")
        return
    
    print(f"\n✓ 총 {len(analyzed_data)}개 통화 분석 완료")
    
    # 3. 모든 통화 시각화
    print("\n[3/4] 그래프 생성 중...")
    visualizer = FXVisualizer(config.GRAPH_CONFIG)
    
    charts_data = {}
    
    try:
        for currency_code, data in analyzed_data.items():
            print(f"  - {data['info']['name']} 그래프 생성 중...")
            
            fig = visualizer.create_trend_chart(
                df=data['df'],
                currency_name=data['info']['name'],
                currency_symbol=data['info']['symbol'],
                ma_config=config.MOVING_AVERAGES,
                statistics=data['statistics']
            )
            
            summary_html = visualizer.create_summary_html(
                statistics=data['statistics'],
                currency_name=data['info']['name']
            )
            
            charts_data[currency_code] = {
                'figure': fig,
                'summary': summary_html,
                'info': data['info'],
                'statistics': data['statistics']
            }
            
            print(f"    ✓ 그래프 생성 완료")
        
        print(f"\n✓ 총 {len(charts_data)}개 통화 그래프 생성 완료")
        
    except Exception as e:
        import traceback
        print(f"✗ 시각화 실패: {str(e)}")
        print("\n상세 오류:")
        traceback.print_exc()
        return
    
    # 4. 다중 통화 HTML 파일 저장
    print("\n[4/4] HTML 파일 저장 중...")
    
    # 출력 디렉토리 생성
    output_dir = Path(config.OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / config.OUTPUT_FILENAME
    
    try:
        visualizer.save_multi_currency_html(
            charts_data=charts_data,
            output_path=str(output_path),
            title="FX Trend Dashboard",
            default_currency=config.DEFAULT_CURRENCY
        )
        print(f"✓ HTML 파일 저장 완료: {output_path}")
    except Exception as e:
        import traceback
        print(f"✗ HTML 저장 실패: {str(e)}")
        traceback.print_exc()
        return
    
    print("\n" + "=" * 60)
    print("✓ FX Trend Dashboard 생성 완료!")
    print("=" * 60)
    print(f"\n생성된 파일: {output_path}")
    print(f"브라우저에서 열어 확인하세요.")


if __name__ == '__main__':
    main()
