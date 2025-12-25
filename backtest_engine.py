"""
Backtest Engine
Executes trades and tracks results
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime


class BacktestEngine:
    """Executes and tracks backtest trades"""
    
    def __init__(self):
        self.trades = []
        
    def execute_trade(self, signal: Dict, data_5m: pd.DataFrame) -> Dict:
        """
        Execute a trade based on signal and track to completion
        
        Args:
            signal: Entry signal dictionary
            data_5m: 5m dataframe for tracking price movement
            
        Returns:
            Completed trade dictionary
        """
        entry_price = signal['entry_price']
        entry_time = signal['entry_time']
        stop_loss = signal['stop_loss']
        direction = signal['direction']
        
        # Get TP levels
        if 'tp1' in signal:
            tp1 = signal['tp1']
            tp2 = signal['tp2']
        else:
            tp1 = signal['tp']
            tp2 = None
        
        # Get data after entry
        post_entry = data_5m[data_5m.index > entry_time]
        
        if len(post_entry) == 0:
            return self._create_incomplete_trade(signal, "NO_DATA")
        
        # Track price movement to find exit
        exit_result = None
        exit_price = None
        exit_time = None
        
        for i in range(len(post_entry)):
            candle = post_entry.iloc[i]
            
            if direction == 'BULLISH':
                # Check stop loss hit
                if candle['Low'] <= stop_loss:
                    exit_result = 'STOP_LOSS'
                    exit_price = stop_loss
                    exit_time = post_entry.index[i]
                    break
                
                # Check TP2 hit first (higher target)
                if tp2 is not None and candle['High'] >= tp2:
                    exit_result = 'TP2'
                    exit_price = tp2
                    exit_time = post_entry.index[i]
                    break
                
                # Check TP1 hit
                if candle['High'] >= tp1:
                    exit_result = 'TP1'
                    exit_price = tp1
                    exit_time = post_entry.index[i]
                    break
            
            elif direction == 'BEARISH':
                # Check stop loss hit
                if candle['High'] >= stop_loss:
                    exit_result = 'STOP_LOSS'
                    exit_price = stop_loss
                    exit_time = post_entry.index[i]
                    break
                
                # Check TP2 hit first (lower target)
                if tp2 is not None and candle['Low'] <= tp2:
                    exit_result = 'TP2'
                    exit_price = tp2
                    exit_time = post_entry.index[i]
                    break
                
                # Check TP1 hit
                if candle['Low'] <= tp1:
                    exit_result = 'TP1'
                    exit_price = tp1
                    exit_time = post_entry.index[i]
                    break
            
            # Max 4 hours (48 x 5m bars)
            if i >= 48:
                # Exit at current price if no target hit
                exit_result = 'TIMEOUT'
                exit_price = candle['Close']
                exit_time = post_entry.index[i]
                break
        
        # If no exit found in available data
        if exit_result is None:
            return self._create_incomplete_trade(signal, "INCOMPLETE")
        
        # Calculate P&L
        if direction == 'BULLISH':
            pnl = exit_price - entry_price
        else:  # BEARISH
            pnl = entry_price - exit_price
        
        # Calculate R:R ratio
        risk = abs(entry_price - stop_loss)
        reward = abs(pnl)
        rr_ratio = reward / risk if risk > 0 else 0
        
        # Build trade record
        trade = {
            'date': signal['date'],
            'strategy': signal['strategy'],
            'entry_time': entry_time,
            'entry_price': entry_price,
            'exit_time': exit_time,
            'exit_price': exit_price,
            'exit_result': exit_result,
            'direction': direction,
            'stop_loss': stop_loss,
            'tp1': tp1,
            'tp2': tp2 if tp2 is not None else 'N/A',
            'pnl': pnl,
            'pnl_pct': (pnl / entry_price) * 100,
            'risk': risk,
            'reward': reward,
            'rr_ratio': rr_ratio,
            'asian_high': signal['asian_high'],
            'asian_low': signal['asian_low'],
            'bias': signal['bias'],
            'win': 1 if pnl > 0 else 0
        }
        
        # Add strategy-specific fields
        if 'entry_type' in signal:
            trade['entry_type'] = signal['entry_type']
        if 'entry_reason' in signal:
            trade['entry_reason'] = signal['entry_reason']
        if 'breakout_strength' in signal:
            trade['breakout_strength'] = signal['breakout_strength']
        
        return trade
    
    def _create_incomplete_trade(self, signal: Dict, reason: str) -> Dict:
        """Create trade record for incomplete/invalid trades"""
        return {
            'date': signal['date'],
            'strategy': signal['strategy'],
            'entry_time': signal['entry_time'],
            'entry_price': signal['entry_price'],
            'exit_time': None,
            'exit_price': None,
            'exit_result': reason,
            'direction': signal['direction'],
            'stop_loss': signal['stop_loss'],
            'tp1': signal.get('tp1', signal.get('tp', 'N/A')),
            'tp2': signal.get('tp2', 'N/A'),
            'pnl': 0,
            'pnl_pct': 0,
            'risk': signal.get('risk', 0),
            'reward': 0,
            'rr_ratio': 0,
            'asian_high': signal['asian_high'],
            'asian_low': signal['asian_low'],
            'bias': signal['bias'],
            'win': 0
        }
    
    def add_market_context(self, trade: Dict) -> Dict:
        """
        Add market context based on date
        
        Args:
            trade: Trade dictionary
            
        Returns:
            Trade with market_context field added
        """
        date_str = trade['date']
        date = pd.to_datetime(date_str).date()
        year = date.year
        month = date.month
        
        context = "Normal Market"
        
        # COVID Crash
        if year == 2020 and month in [2, 3, 4]:
            context = "COVID Crash (High Volatility)"
        
        # COVID Recovery
        elif year == 2020 and month in [5, 6, 7, 8, 9, 10, 11, 12]:
            context = "COVID Recovery Rally"
        
        # 2021 Bull Market
        elif year == 2021:
            context = "Bull Market 2021"
        
        # 2022 Bear Market
        elif year == 2022:
            context = "Bear Market 2022 (Fed Tightening)"
        
        # 2023 Recovery
        elif year == 2023:
            context = "2023 Recovery (AI Rally)"
        
        # 2024-2025
        elif year >= 2024:
            context = "Recent Market 2024-2025"
        
        trade['market_context'] = context
        return trade
    
    def get_results_dataframe(self) -> pd.DataFrame:
        """
        Convert trades list to DataFrame
        
        Returns:
            DataFrame with all trade results
        """
        if not self.trades:
            return pd.DataFrame()
        
        return pd.DataFrame(self.trades)
    
    def calculate_statistics(self) -> Dict:
        """
        Calculate performance statistics
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.trades:
            return {}
        
        df = self.get_results_dataframe()
        
        # Filter valid trades (exclude incomplete/timeout)
        valid_trades = df[df['exit_result'].isin(['TP1', 'TP2', 'STOP_LOSS'])]
        
        if len(valid_trades) == 0:
            return {'error': 'No valid trades'}
        
        stats = {
            'total_signals': len(df),
            'valid_trades': len(valid_trades),
            'total_wins': valid_trades['win'].sum(),
            'total_losses': len(valid_trades) - valid_trades['win'].sum(),
            'win_rate': (valid_trades['win'].sum() / len(valid_trades) * 100) if len(valid_trades) > 0 else 0,
            'avg_rr_ratio': valid_trades['rr_ratio'].mean(),
            'avg_pnl': valid_trades['pnl'].mean(),
            'total_pnl': valid_trades['pnl'].sum(),
            'max_win': valid_trades['pnl'].max(),
            'max_loss': valid_trades['pnl'].min(),
            'avg_win': valid_trades[valid_trades['win'] == 1]['pnl'].mean() if len(valid_trades[valid_trades['win'] == 1]) > 0 else 0,
            'avg_loss': valid_trades[valid_trades['win'] == 0]['pnl'].mean() if len(valid_trades[valid_trades['win'] == 0]) > 0 else 0,
        }
        
        # Strategy breakdown
        for strategy in df['strategy'].unique():
            strategy_trades = valid_trades[valid_trades['strategy'] == strategy]
            if len(strategy_trades) > 0:
                stats[f'{strategy}_trades'] = len(strategy_trades)
                stats[f'{strategy}_win_rate'] = (strategy_trades['win'].sum() / len(strategy_trades) * 100)
                stats[f'{strategy}_avg_rr'] = strategy_trades['rr_ratio'].mean()
                stats[f'{strategy}_total_pnl'] = strategy_trades['pnl'].sum()
        
        return stats


if __name__ == "__main__":
    print("Backtest Engine Module")
    print("="*50)
    print("Module loaded successfully")
