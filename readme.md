# Trade Raider

A cozy, pixel-flavored stock trading sim with 125 fictional companies. Start with $25,000, trade weekly, read the headlines, and try to reach $1,000,000.

## Features
- **125 fake companies** generated fresh each run with unique names, sectors, volatility, and signature traits.
- **Rotating hype themes** each week that favor matching traits for an ever-changing market mood.
- **News-driven swings** with positive and negative headlines that jolt prices and surface top movers.
- **Simple terminal play**: buy or sell tickers, advance a week, and watch your portfolio grow (or crater).

## Play
```bash
python game.py
```

You'll see a market glance with sample tickers, your portfolio, and options:
- `B` to buy shares of a ticker.
- `S` to sell shares you own.
- `A` to advance a week and reveal the news.
- `Q` to exit.

Win by pushing your net worth above **$1,000,000**. Every session builds a new market so runs stay fresh.
