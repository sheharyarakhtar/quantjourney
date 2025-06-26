# QuantJourney

A comprehensive quantitative trading and financial analysis repository documenting various trading strategies, market analysis, and algorithmic trading approaches.

## 📁 Repository Structure

```
quantjourney/
├── 📊 analysis/                    # Market analysis notebooks
│   ├── stocks/                     # Stock market analysis
│   ├── crypto/                     # Cryptocurrency analysis
│   └── market_regime/              # Market regime detection
├── 🤖 models/                      # Trading models and strategies
│   ├── fourier/                    # FFT-based models
│   ├── monte_carlo/                # Monte Carlo simulations
│   ├── bayesian/                   # Bayesian models (PyMC)
│   └── hft/                        # High-frequency trading
├── 📈 backtesting/                 # Strategy backtesting
│   ├── backtrader/                 # Backtrader framework
│   └── custom/                     # Custom backtesting
├── 🛠️ utils/                       # Utility functions and tools
│   ├── data/                       # Data handling utilities
│   ├── visualization/              # Plotting and charts
│   └── deployment/                 # Docker and deployment
├── 📋 data/                        # Data storage
│   ├── raw/                        # Raw data files
│   ├── processed/                  # Processed datasets
│   └── models/                     # Saved model files
├── 📚 docs/                        # Documentation
├── 🧪 tests/                       # Unit tests
└── 📦 config/                      # Configuration files
```

## 🚀 Quick Start

1. **Setup Environment**:
   ```bash
   conda env create -f utils/env.yml
   conda activate quantjourney
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r utils/requirements.txt
   ```

3. **Download Data**:
   ```bash
   python utils/data/download_data.py
   ```

## 📊 Analysis Categories

### Stocks
- **Technical Analysis**: FFT modeling, regime detection
- **Statistical Models**: Monte Carlo simulations, Bayesian AR models
- **High-Frequency Trading**: HFT strategies and analysis

### Cryptocurrency
- **Market Analysis**: Binance data analysis, order book analysis
- **Pricing Models**: Cryptocurrency pricing and volatility analysis
- **Arbitrage**: Cross-exchange arbitrage opportunities

## 🤖 Models

- **Fourier Transform Models**: Frequency domain analysis for time series
- **Monte Carlo Simulations**: Risk assessment and option pricing
- **Bayesian Models**: Probabilistic forecasting with PyMC
- **HFT Strategies**: High-frequency trading algorithms

## 🛠️ Utilities

- **Data Management**: Automated data downloading and processing
- **Visualization**: Custom plotting functions for financial data
- **Deployment**: Docker configuration for containerized execution

## 📈 Backtesting

- **Backtrader Framework**: Standardized backtesting environment
- **Custom Strategies**: Proprietary backtesting implementations

## 🤝 Contributing

1. Follow the established directory structure
2. Use descriptive names for notebooks and scripts
3. Include documentation for complex models
4. Add tests for utility functions

## 📝 License

This project is for educational and research purposes in quantitative finance.
