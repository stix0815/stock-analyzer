"""
Quick demo of fundamental analysis output
Shows what users will see for different stock types
"""
from fundamentals import FundamentalAnalyzer


def demo_stock(ticker, description):
    """Show key fundamental insights for a stock."""
    print(f"\n{'='*80}")
    print(f"{ticker} - {description}")
    print('='*80)
    
    analyzer = FundamentalAnalyzer(ticker)
    fundamentals = analyzer.fetch_fundamentals()
    health_score, analysis = analyzer.calculate_health_score(fundamentals)
    
    # Overall assessment
    if health_score >= 70:
        emoji = "🟢"
        rating = "STRONG BUY for long-term"
    elif health_score >= 50:
        emoji = "🟡"
        rating = "HOLD / Moderate buy"
    else:
        emoji = "🔴"
        rating = "CAUTION / High risk"
    
    print(f"\n{emoji} Health Score: {health_score}/100 - {rating}")
    print(f"💰 Valuation: {analysis['valuation_status']}")
    
    # Quick snapshot of key metrics
    val = fundamentals['valuation']
    prof = fundamentals['profitability']
    growth = fundamentals['growth']
    health_data = fundamentals['financial_health']
    
    print(f"\n📊 KEY METRICS SNAPSHOT:")
    pe = val.get('pe_trailing')
    peg = val.get('peg_ratio')
    de = health_data.get('debt_to_equity')
    cr = health_data.get('current_ratio')
    
    pe_str = f"{pe:.1f}" if pe else "N/A"
    peg_str = f"{peg:.2f}" if peg else "N/A"
    de_str = f"{de:.1f}" if de is not None else "N/A"
    cr_str = f"{cr:.2f}" if cr else "N/A"
    
    print(f"  Valuation:  P/E={pe_str} | PEG={peg_str}")
    print(f"  Profit:     Margin={prof.get('profit_margin', 0)*100:.1f}% | ROE={prof.get('roe', 0)*100:.1f}%")
    print(f"  Growth:     Revenue={growth.get('revenue_growth', 0)*100:.1f}% | Earnings={growth.get('earnings_growth', 0)*100:.1f}%")
    print(f"  Health:     D/E={de_str} | Current Ratio={cr_str}")
    
    # Top insights
    print(f"\n✅ TOP STRENGTHS:")
    for i, strength in enumerate(analysis['strengths'][:3], 1):
        print(f"  {i}. {strength}")
    
    if analysis['red_flags']:
        print(f"\n🚩 TOP RED FLAGS:")
        for i, flag in enumerate(analysis['red_flags'][:3], 1):
            print(f"  {i}. {flag}")
    else:
        print(f"\n✅ No major red flags!")
    
    # Investment recommendation
    print(f"\n💡 INVESTMENT INSIGHT:")
    if health_score >= 70:
        print("   Strong fundamentals make this suitable for long-term portfolios.")
        print("   Consider dollar-cost averaging for entry. Monitor quarterly earnings.")
    elif health_score >= 50:
        print("   Mixed fundamentals require deeper analysis. Compare to peers.")
        print("   Suitable for experienced investors willing to accept moderate risk.")
    else:
        print("   Weak fundamentals suggest high risk. Only for speculative positions.")
        print("   Look for turnaround catalysts. Use strict position sizing & stops.")


def main():
    """Run demonstration."""
    print("="*80)
    print("FUNDAMENTAL ANALYSIS FEATURE - USER EXPERIENCE DEMO")
    print("="*80)
    print("\nShowing what users will see in the new 📈 Fundamentals tab...")
    
    demo_stock("AAPL", "Mature Tech Giant")
    demo_stock("NVDA", "High-Growth AI Leader")
    demo_stock("JNJ", "Dividend Aristocrat")
    
    print(f"\n{'='*80}")
    print("DEMO COMPLETE")
    print('='*80)
    print("\n✅ Users now have comprehensive fundamental analysis alongside technical indicators!")
    print("✅ Perfect for making informed long-term investment decisions!")


if __name__ == "__main__":
    main()
