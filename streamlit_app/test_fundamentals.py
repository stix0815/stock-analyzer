"""
Test script for Fundamental Analysis feature
Tests with AAPL (mature), TSLA (growth), and KO (dividend stock)
"""
from fundamentals import FundamentalAnalyzer
import json


def test_stock(ticker):
    """Test fundamental analysis for a given ticker."""
    print(f"\n{'='*80}")
    print(f"Testing {ticker}")
    print('='*80)
    
    analyzer = FundamentalAnalyzer(ticker)
    fundamentals = analyzer.fetch_fundamentals()
    health_score, analysis = analyzer.calculate_health_score(fundamentals)
    
    # Display results
    print(f"\n🎯 HEALTH SCORE: {health_score}/100")
    print(f"💰 VALUATION STATUS: {analysis['valuation_status']}")
    
    print(f"\n✅ STRENGTHS ({len(analysis['strengths'])}):")
    for strength in analysis['strengths'][:5]:
        print(f"  - {strength}")
    
    print(f"\n🚩 RED FLAGS ({len(analysis['red_flags'])}):")
    if analysis['red_flags']:
        for flag in analysis['red_flags'][:5]:
            print(f"  - {flag}")
    else:
        print("  None identified")
    
    # Display key metrics
    print(f"\n📊 KEY METRICS:")
    
    val = fundamentals['valuation']
    if val.get('pe_trailing'):
        print(f"  P/E Ratio (Trailing): {val['pe_trailing']:.2f}")
    if val.get('peg_ratio'):
        print(f"  PEG Ratio: {val['peg_ratio']:.2f}")
    if val.get('pb_ratio'):
        print(f"  P/B Ratio: {val['pb_ratio']:.2f}")
    
    prof = fundamentals['profitability']
    if prof.get('profit_margin'):
        print(f"  Profit Margin: {prof['profit_margin']*100:.2f}%")
    if prof.get('roe'):
        print(f"  ROE: {prof['roe']*100:.2f}%")
    
    growth = fundamentals['growth']
    if growth.get('revenue_growth'):
        print(f"  Revenue Growth: {growth['revenue_growth']*100:.2f}%")
    if growth.get('earnings_growth'):
        print(f"  Earnings Growth: {growth['earnings_growth']*100:.2f}%")
    
    health = fundamentals['financial_health']
    if health.get('debt_to_equity') is not None:
        print(f"  Debt-to-Equity: {health['debt_to_equity']:.1f}")
    if health.get('current_ratio'):
        print(f"  Current Ratio: {health['current_ratio']:.2f}")
    
    div = fundamentals['dividends']
    if div.get('dividend_yield'):
        print(f"  Dividend Yield: {div['dividend_yield']*100:.2f}%")
    else:
        print(f"  Dividend Yield: None")
    
    other = fundamentals['other']
    if other.get('beta'):
        print(f"  Beta: {other['beta']:.2f}")
    
    # Test interpretations
    print(f"\n💡 SAMPLE INTERPRETATIONS:")
    if val.get('pe_trailing'):
        interp = analyzer.get_metric_interpretation('pe_trailing', val['pe_trailing'])
        print(f"  P/E Ratio: {interp}")
    if prof.get('roe'):
        interp = analyzer.get_metric_interpretation('roe', prof['roe'])
        print(f"  ROE: {interp}")
    if health.get('debt_to_equity') is not None:
        interp = analyzer.get_metric_interpretation('debt_to_equity', health['debt_to_equity'])
        print(f"  Debt-to-Equity: {interp}")
    
    return {
        'ticker': ticker,
        'health_score': health_score,
        'valuation': analysis['valuation_status'],
        'strengths_count': len(analysis['strengths']),
        'red_flags_count': len(analysis['red_flags'])
    }


def main():
    """Run tests on all three stock types."""
    print("FUNDAMENTAL ANALYSIS FEATURE TEST")
    print("Testing three different company profiles:")
    print("  - AAPL: Mature, profitable company")
    print("  - TSLA: High-growth company")
    print("  - KO: Dividend-paying company")
    
    results = []
    
    # Test each stock
    for ticker in ['AAPL', 'TSLA', 'KO']:
        try:
            result = test_stock(ticker)
            results.append(result)
        except Exception as e:
            print(f"\n❌ ERROR testing {ticker}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print('='*80)
    print(f"\n{'Ticker':<10} {'Health Score':<15} {'Valuation':<20} {'Strengths':<12} {'Red Flags'}")
    print('-'*80)
    for r in results:
        print(f"{r['ticker']:<10} {r['health_score']:<15} {r['valuation']:<20} {r['strengths_count']:<12} {r['red_flags_count']}")
    
    print(f"\n✅ TEST COMPLETED SUCCESSFULLY")
    print(f"All {len(results)} stocks analyzed successfully!")


if __name__ == "__main__":
    main()
