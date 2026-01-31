"""
Monte Carlo simulation for stock price prediction.
"""
import numpy as np
import pandas as pd
from typing import Dict, Tuple


class MonteCarloSimulator:
    """Run Monte Carlo simulations for stock price predictions."""
    
    def __init__(self, data: pd.DataFrame, iterations: int = 1000):
        """
        Initialize Monte Carlo simulator.
        
        Args:
            data: Historical price data
            iterations: Number of simulation iterations
        """
        self.data = data
        self.iterations = iterations
        
    def run_simulation(self, days: int, current_price: float) -> Dict:
        """
        Run Monte Carlo simulation.
        
        Args:
            days: Number of days to simulate
            current_price: Starting price
            
        Returns:
            Dictionary with simulation results
        """
        # Calculate historical returns
        returns = self.data['Close'].pct_change().dropna()
        
        # Calculate drift (mean return) and volatility (std of returns)
        drift = returns.mean()
        volatility = returns.std()
        
        # Run simulations
        simulations = np.zeros((self.iterations, days))
        
        for i in range(self.iterations):
            # Generate random returns based on historical distribution
            daily_returns = np.random.normal(drift, volatility, days)
            
            # Calculate price path
            price_path = [current_price]
            for ret in daily_returns:
                price_path.append(price_path[-1] * (1 + ret))
            
            simulations[i] = price_path[1:]  # Exclude starting price
        
        # Calculate statistics
        final_prices = simulations[:, -1]
        
        # Calculate probabilities
        bull_prob, bear_prob = self._calculate_probabilities(final_prices, current_price)
        
        # Calculate price targets
        median_price = np.median(final_prices)
        mean_price = np.mean(final_prices)
        percentile_10 = np.percentile(final_prices, 10)
        percentile_90 = np.percentile(final_prices, 90)
        
        # Bull/bear scenarios
        bull_target = np.percentile(final_prices, 65)
        bear_target = np.percentile(final_prices, 35)
        
        return {
            'simulations': simulations,
            'final_prices': final_prices,
            'median_price': median_price,
            'mean_price': mean_price,
            'percentile_10': percentile_10,
            'percentile_90': percentile_90,
            'bull_probability': bull_prob,
            'bear_probability': bear_prob,
            'bull_target': bull_target,
            'bear_target': bear_target,
            'drift': drift,
            'volatility': volatility,
            'current_price': current_price,
            'days': days
        }
    
    def _calculate_probabilities(self, final_prices: np.ndarray, current_price: float) -> Tuple[float, float]:
        """
        Calculate bull and bear probabilities.
        
        Args:
            final_prices: Array of simulated final prices
            current_price: Current stock price
            
        Returns:
            Tuple of (bull_probability, bear_probability)
        """
        # Bull: price goes up
        bull_count = np.sum(final_prices > current_price)
        bull_prob = (bull_count / len(final_prices)) * 100
        
        # Bear: price goes down
        bear_prob = 100 - bull_prob
        
        return bull_prob, bear_prob
    
    def get_scenarios(self, simulation_results: Dict) -> Dict:
        """
        Generate bull and bear scenario descriptions.
        
        Args:
            simulation_results: Results from run_simulation
            
        Returns:
            Dictionary with scenario descriptions
        """
        current = simulation_results['current_price']
        bull_target = simulation_results['bull_target']
        bear_target = simulation_results['bear_target']
        days = simulation_results['days']
        
        bull_change = ((bull_target - current) / current) * 100
        bear_change = ((bear_target - current) / current) * 100
        
        return {
            'bull': {
                'probability': simulation_results['bull_probability'],
                'target': bull_target,
                'change_pct': bull_change,
                'days': days,
                'description': f"Target: ${bull_target:.2f} ({bull_change:+.1f}%) in {days} days"
            },
            'bear': {
                'probability': simulation_results['bear_probability'],
                'target': bear_target,
                'change_pct': bear_change,
                'days': days,
                'description': f"Risk: ${bear_target:.2f} ({bear_change:+.1f}%) if support breaks"
            }
        }
