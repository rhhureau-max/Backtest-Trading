================================================================================
NQ LONDON CONTINUATION + INVERSION FVG - ANALYSIS REPORT
================================================================================

QUESTION 1: Retest Entry vs Immediate Entry
--------------------------------------------------------------------------------
Does waiting for a retest of the Inversion FVG reduce drawdown?

Configuration: SL_A_asian_high
  Immediate Entry:
    Trades: 44, Win Rate: 29.5%
    Expectancy: -10.22 pts, Max DD: -481.24 pts
  Retest Entry:
    Trades: 37, Win Rate: 18.9%
    Expectancy: 1.61 pts, Max DD: -123.17 pts
  Difference:
    Win Rate: -10.6%
    Expectancy: +11.83 pts
    Max DD: +358.07 pts

Configuration: SL_A_fixed_10
  Immediate Entry:
    Trades: 45, Win Rate: 53.3%
    Expectancy: 1.59 pts, Max DD: -36.16 pts
  Retest Entry:
    Trades: 37, Win Rate: 35.1%
    Expectancy: -0.12 pts, Max DD: -56.55 pts
  Difference:
    Win Rate: -18.2%
    Expectancy: -1.71 pts
    Max DD: -20.38 pts

Configuration: SL_A_fixed_15
  Immediate Entry:
    Trades: 45, Win Rate: 44.4%
    Expectancy: 1.48 pts, Max DD: -50.77 pts
  Retest Entry:
    Trades: 37, Win Rate: 29.7%
    Expectancy: 0.43 pts, Max DD: -41.55 pts
  Difference:
    Win Rate: -14.7%
    Expectancy: -1.05 pts
    Max DD: +9.22 pts

Configuration: SL_A_fixed_20
  Immediate Entry:
    Trades: 45, Win Rate: 33.3%
    Expectancy: -0.37 pts, Max DD: -117.71 pts
  Retest Entry:
    Trades: 37, Win Rate: 24.3%
    Expectancy: 0.25 pts, Max DD: -71.26 pts
  Difference:
    Win Rate: -9.0%
    Expectancy: +0.62 pts
    Max DD: +46.46 pts

Configuration: SL_B_asian_high
  Immediate Entry:
    Trades: 43, Win Rate: 60.5%
    Expectancy: -3.62 pts, Max DD: -344.23 pts
  Retest Entry:
    Trades: 36, Win Rate: 52.8%
    Expectancy: 4.02 pts, Max DD: -129.99 pts
  Difference:
    Win Rate: -7.7%
    Expectancy: +7.64 pts
    Max DD: +214.24 pts


QUESTION 2: SL A (Aggressive) vs SL B (Structural)
--------------------------------------------------------------------------------
Is the aggressive stop loss viable on NQ, or is structural better?

Configuration: asian_high_immediate
  SL A (Aggressive):
    Win Rate: 29.5%, Expectancy: -10.22 pts
    Profit Factor: -0.25, Avg Risk: 13.58 pts
  SL B (Structural):
    Win Rate: 60.5%, Expectancy: -3.62 pts
    Profit Factor: 0.76, Avg Risk: 42.92 pts
  Winner: SL B (+6.60 pts expectancy)

Configuration: asian_high_retest
  SL A (Aggressive):
    Win Rate: 18.9%, Expectancy: 1.61 pts
    Profit Factor: 1.29, Avg Risk: 6.66 pts
  SL B (Structural):
    Win Rate: 52.8%, Expectancy: 4.02 pts
    Profit Factor: 1.24, Avg Risk: 32.51 pts
  Winner: SL B (+2.42 pts expectancy)

Configuration: fixed_10_immediate
  SL A (Aggressive):
    Win Rate: 53.3%, Expectancy: 1.59 pts
    Profit Factor: 1.42, Avg Risk: 14.37 pts
  SL B (Structural):
    Win Rate: 75.6%, Expectancy: 0.17 pts
    Profit Factor: 1.02, Avg Risk: 44.30 pts
  Winner: SL A (+1.42 pts expectancy)

Configuration: fixed_15_immediate
  SL A (Aggressive):
    Win Rate: 44.4%, Expectancy: 1.48 pts
    Profit Factor: 1.29, Avg Risk: 14.37 pts
  SL B (Structural):
    Win Rate: 68.9%, Expectancy: 0.85 pts
    Profit Factor: 1.09, Avg Risk: 44.30 pts
  Winner: SL A (+0.63 pts expectancy)

Configuration: fixed_20_immediate
  SL A (Aggressive):
    Win Rate: 33.3%, Expectancy: -0.37 pts
    Profit Factor: 0.95, Avg Risk: 14.37 pts
  SL B (Structural):
    Win Rate: 64.4%, Expectancy: 0.93 pts
    Profit Factor: 1.08, Avg Risk: 44.30 pts
  Winner: SL B (+1.30 pts expectancy)


QUESTION 3: Target Optimization
--------------------------------------------------------------------------------
Asian High vs Fixed Targets (10/15/20 pts)

Configuration: SL_A_immediate
  asian_high:
    Win Rate: 29.5%, Expectancy: -10.22 pts
    Profit Factor: -0.25
  fixed_10:
    Win Rate: 53.3%, Expectancy: 1.59 pts
    Profit Factor: 1.42
  fixed_15:
    Win Rate: 44.4%, Expectancy: 1.48 pts
    Profit Factor: 1.29
  fixed_20:
    Win Rate: 33.3%, Expectancy: -0.37 pts
    Profit Factor: 0.95
  Best Target: fixed_10 (1.59 pts expectancy)

Configuration: SL_A_retest
  asian_high:
    Win Rate: 18.9%, Expectancy: 1.61 pts
    Profit Factor: 1.29
  fixed_10:
    Win Rate: 35.1%, Expectancy: -0.12 pts
    Profit Factor: 0.97
  fixed_15:
    Win Rate: 29.7%, Expectancy: 0.43 pts
    Profit Factor: 1.11
  fixed_20:
    Win Rate: 24.3%, Expectancy: 0.25 pts
    Profit Factor: 1.05
  Best Target: asian_high (1.61 pts expectancy)

Configuration: SL_B_immediate
  asian_high:
    Win Rate: 60.5%, Expectancy: -3.62 pts
    Profit Factor: 0.76
  fixed_10:
    Win Rate: 75.6%, Expectancy: 0.17 pts
    Profit Factor: 1.02
  fixed_15:
    Win Rate: 68.9%, Expectancy: 0.85 pts
    Profit Factor: 1.09
  fixed_20:
    Win Rate: 64.4%, Expectancy: 0.93 pts
    Profit Factor: 1.08
  Best Target: fixed_20 (0.93 pts expectancy)

Configuration: SL_B_retest
  asian_high:
    Win Rate: 52.8%, Expectancy: 4.02 pts
    Profit Factor: 1.24
  Best Target: asian_high (4.02 pts expectancy)


================================================================================
SUMMARY AND RECOMMENDATIONS
================================================================================

BEST CONFIGURATION: SL_B_asian_high_retest
  Win Rate: 52.8%
  Expectancy: 4.02 pts
  Profit Factor: 1.24
  Total Trades: 36
  Total P&L: 144.80 pts

================================================================================