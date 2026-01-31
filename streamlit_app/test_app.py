"""
Quick test script to verify all modules work correctly.
"""
import sys

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from data_fetcher import DataFetcher
        print("✓ data_fetcher imported successfully")
    except Exception as e:
        print(f"✗ data_fetcher import failed: {e}")
        return False
    
    try:
        from indicators import TechnicalIndicators
        print("✓ indicators imported successfully")
    except Exception as e:
        print(f"✗ indicators import failed: {e}")
        return False
    
    try:
        from scoring import ScoringSystem
        print("✓ scoring imported successfully")
    except Exception as e:
        print(f"✗ scoring import failed: {e}")
        return False
    
    try:
        from monte_carlo import MonteCarloSimulator
        print("✓ monte_carlo imported successfully")
    except Exception as e:
        print(f"✗ monte_carlo import failed: {e}")
        return False
    
    return True


def test_data_fetch():
    """Test data fetching with AAPL."""
    print("\nTesting data fetch for AAPL...")
    
    try:
        from data_fetcher import DataFetcher
        
        fetcher = DataFetcher("AAPL")
        
        # Validate ticker
        if not fetcher.validate_ticker():
            print("✗ Ticker validation failed")
            return False
        print("✓ Ticker validation passed")
        
        # Fetch data
        data = fetcher.fetch_data("short")
        if data is None or data.empty:
            print("✗ Data fetch returned empty")
            return False
        print(f"✓ Data fetched: {len(data)} rows")
        
        # Get stock info
        info = fetcher.get_stock_info()
        print(f"✓ Stock info retrieved: {info['name']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Data fetch test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_indicators():
    """Test technical indicators calculation."""
    print("\nTesting technical indicators...")
    
    try:
        from data_fetcher import DataFetcher
        from indicators import TechnicalIndicators
        
        fetcher = DataFetcher("AAPL")
        data = fetcher.fetch_data("short")
        
        calc = TechnicalIndicators(data)
        indicators = calc.calculate_all()
        
        # Check all indicators are present
        required = ['rsi', 'macd', 'bollinger', 'sma', 'volume']
        for ind in required:
            if ind not in indicators:
                print(f"✗ Missing indicator: {ind}")
                return False
        
        print(f"✓ All indicators calculated")
        print(f"  - RSI: {indicators['rsi']['value']:.2f}")
        print(f"  - MACD Signal: {indicators['macd']['signal']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Indicators test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scoring():
    """Test scoring system."""
    print("\nTesting scoring system...")
    
    try:
        from data_fetcher import DataFetcher
        from indicators import TechnicalIndicators
        from scoring import ScoringSystem
        
        fetcher = DataFetcher("AAPL")
        data = fetcher.fetch_data("short")
        info = fetcher.get_stock_info()
        
        calc = TechnicalIndicators(data)
        indicators = calc.calculate_all()
        
        scorer = ScoringSystem("short", "moderate")
        results = scorer.calculate_score(indicators, info)
        
        print(f"✓ Score calculated: {results['score']}/100")
        print(f"  - Signal: {results['signal']}")
        print(f"  - Confidence: {results['confidence']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Scoring test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_monte_carlo():
    """Test Monte Carlo simulation."""
    print("\nTesting Monte Carlo simulation...")
    
    try:
        from data_fetcher import DataFetcher
        from monte_carlo import MonteCarloSimulator
        
        fetcher = DataFetcher("AAPL")
        data = fetcher.fetch_data("short")
        info = fetcher.get_stock_info()
        
        sim = MonteCarloSimulator(data, iterations=100)  # Use fewer for testing
        results = sim.run_simulation(7, info['current_price'])
        scenarios = sim.get_scenarios(results)
        
        print(f"✓ Monte Carlo simulation completed")
        print(f"  - Bull probability: {scenarios['bull']['probability']:.1f}%")
        print(f"  - Bear probability: {scenarios['bear']['probability']:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"✗ Monte Carlo test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Stock Analysis App - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Data Fetch", test_data_fetch),
        ("Indicators", test_indicators),
        ("Scoring", test_scoring),
        ("Monte Carlo", test_monte_carlo),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("The app is ready to run: streamlit run app.py")
    else:
        print("✗ SOME TESTS FAILED")
        print("Please check the errors above")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
