#!/usr/bin/env python3
"""
Trade Raider: a playful pixel-flavored stock trading sim with fake companies.

Run with:
    python game.py

The game generates a fresh set of 125 fictional tickers every session, each
with unique traits and volatility. Start with $25,000 and try to reach $1,000,000
by buying and selling weekly. Headlines and rotating themes sway prices so every
run feels different.
"""
from __future__ import annotations

import random
import textwrap
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

SECTORS = [
    "Tech", "Energy", "Health", "Retail", "Gaming", "Transport", "Media",
    "Crypto", "Real Estate", "Green", "Defense", "Food", "Robotics",
    "Aerospace", "Finance",
]

TRAITS = [
    "AI Glow", "Dividend Darling", "Turnaround", "Meme Momentum",
    "Steady Eddy", "Cloud Native", "Quantum Curious", "VR Dreamer",
    "Retro Revival", "Logistics Legend", "Eco Innovator", "Biotech Hope",
    "Space Tourist", "Battery Buff", "Streaming Star", "Privacy First",
]

POSITIVE_EVENTS = [
    ("beats earnings", 0.07, 0.18),
    ("unveils a cult-hit product", 0.08, 0.22),
    ("lands a mega-contract", 0.06, 0.16),
    ("goes viral on holo-social", 0.05, 0.14),
    ("wins regulatory fast-track", 0.05, 0.18),
]

NEGATIVE_EVENTS = [
    ("misses guidance", -0.16, -0.05),
    ("faces a recall", -0.22, -0.08),
    ("CEO rage-quits on stream", -0.25, -0.1),
    ("servers melt down", -0.18, -0.05),
    ("hit by surprise fees", -0.14, -0.04),
]

PIXEL_BANNER = r"""
███████╗████████╗ █████╗ ██████╗ ███████╗    ██████╗  █████╗ ██╗██████╗ ███████╗██████╗ 
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
█████╗     ██║   ███████║██████╔╝█████╗      ██████╔╝███████║██║██║  ██║█████╗  ██████╔╝
██╔══╝     ██║   ██╔══██║██╔══██╗██╔══╝      ██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
██║        ██║   ██║  ██║██║  ██║███████╗    ██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║
╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
"""


@dataclass
class Company:
    ticker: str
    name: str
    sector: str
    trait: str
    price: float
    volatility: float
    momentum: float
    last_price: float = field(default=0.0)

    def record_price(self) -> None:
        self.last_price = self.price

    def apply_change(self, pct_change: float) -> None:
        new_price = max(0.5, round(self.price * (1 + pct_change), 2))
        self.price = new_price

    @property
    def weekly_change(self) -> float:
        if self.last_price == 0:
            return 0.0
        return (self.price - self.last_price) / self.last_price


def generate_company_names(count: int) -> List[str]:
    adjectives = [
        "Pixel", "Neon", "Rusty", "Turbo", "Lucky", "Laser", "Quirk",
        "Amber", "Mystic", "Foam", "Glitch", "Lucid", "Drift", "Bronze",
        "Astral", "Solar", "Frost", "Volt", "Echo", "Magma", "Helix",
        "Nimbus", "Nifty", "Nova", "Syrup", "Titan", "Vapor", "Nimbus",
    ]
    nouns = [
        "Anvil", "Bazaar", "Circuit", "Dive", "Empire", "Forge", "Grove",
        "Harbor", "Isotope", "Junction", "Kite", "Lab", "Mint", "Nest",
        "Orbit", "Pulse", "Queue", "Rocket", "Spire", "Trove", "Union",
        "Vault", "Ward", "Yonder", "Zephyr", "Yard", "Crest", "Beacon",
    ]

    names = set()
    while len(names) < count:
        names.add(f"{random.choice(adjectives)} {random.choice(nouns)}")
    return list(names)


def generate_ticker(name: str, idx: int) -> str:
    base = "".join([part[0] for part in name.split()])[:3].upper()
    return f"{base}{idx:02d}"


def generate_companies(count: int = 125) -> List[Company]:
    names = generate_company_names(count)
    companies: List[Company] = []
    for idx, name in enumerate(names):
        ticker = generate_ticker(name, idx)
        sector = random.choice(SECTORS)
        trait = random.choice(TRAITS)
        price = round(random.uniform(8, 90), 2)
        volatility = random.uniform(0.03, 0.18)
        momentum = random.uniform(-0.02, 0.05)
        companies.append(Company(ticker, name, sector, trait, price, volatility, momentum))
    return companies


def describe_theme(trait: str) -> str:
    return {
        "AI Glow": "algorithms sparkle; anything smart gets a boost",
        "Dividend Darling": "yield-chasers pile in for steady payers",
        "Turnaround": "turnaround narratives get a sympathy bump",
        "Meme Momentum": "chat rooms ignite anything with a funny ticker",
        "Steady Eddy": "low-vol grinders are in vogue",
        "Cloud Native": "distributed everything is hot again",
        "Quantum Curious": "qubits trend on holo-feeds",
        "VR Dreamer": "immersive plays get extra hype",
        "Retro Revival": "old-school brands are trendy",
        "Logistics Legend": "supply-chain fixes earn applause",
        "Eco Innovator": "green tech dominates headlines",
        "Biotech Hope": "miracle trials stir optimism",
        "Space Tourist": "off-planet trips get booked solid",
        "Battery Buff": "longer life cells are coveted",
        "Streaming Star": "content libraries binge towards profits",
        "Privacy First": "secure-by-default vendors shine",
    }.get(trait, "weirdly specific hype cycle in play")


def pick_weekly_theme(last_theme: str | None) -> str:
    choices = [t for t in TRAITS if t != last_theme]
    return random.choice(choices)


def generate_news(companies: List[Company]) -> List[Tuple[Company, float, str]]:
    news_items: List[Tuple[Company, float, str]] = []
    headlines = POSITIVE_EVENTS + NEGATIVE_EVENTS
    event_count = random.randint(6, 10)
    picks = random.sample(companies, k=min(event_count, len(companies)))
    for company in picks:
        verb, low, high = random.choice(headlines)
        delta = random.uniform(low, high)
        direction = "soars" if delta > 0 else "slides"
        headline = f"{company.ticker} {verb}; stock {direction}"
        news_items.append((company, delta, headline))
    return news_items


def apply_weekly_changes(
    companies: List[Company],
    weekly_theme: str,
) -> Tuple[List[str], List[Company]]:
    news = generate_news(companies)
    news_copy = list(news)

    for company in companies:
        company.record_price()
        base_noise = random.gauss(0, company.volatility)
        momentum = company.momentum
        trait_bonus = 0.02 if company.trait == weekly_theme else 0.0
        event_boost = 0.0
        for item_company, delta, _ in news_copy:
            if item_company is company:
                event_boost += delta
        pct_change = base_noise + momentum + trait_bonus + event_boost
        pct_change = max(min(pct_change, 0.8), -0.8)
        company.apply_change(pct_change)

    headlines = [h for *_rest, h in news_copy]
    movers = sorted(companies, key=lambda c: c.weekly_change, reverse=True)
    return headlines, movers


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def display_market(companies: List[Company], weekly_theme: str) -> None:
    print("\n=== Pixel Market Glance ===")
    print(f"Theme: {weekly_theme} — {describe_theme(weekly_theme)}")
    sample = sorted(random.sample(companies, k=10), key=lambda c: c.price)
    for company in sample:
        trend = "▲" if company.momentum >= 0 else "▼"
        print(
            f"{company.ticker:<6} {company.price:>7.2f}  {company.sector:<12} {company.trait:<15}  momentum {trend}"
        )


def display_portfolio(
    portfolio: Dict[str, int],
    cash: float,
    companies: Dict[str, Company],
) -> None:
    print("\n=== Portfolio ===")
    print(f"Cash: {format_currency(cash)}")
    total_value = cash
    for ticker, shares in portfolio.items():
        company = companies[ticker]
        value = shares * company.price
        total_value += value
        change = company.weekly_change * 100
        print(
            f"{ticker:<6} {shares:>5} sh  @{company.price:>7.2f}  value {format_currency(value):>10}  weekly {change:+5.1f}%"
        )
    print(f"Total value: {format_currency(total_value)}")


def prompt_ticker(companies: Dict[str, Company]) -> str | None:
    ticker = input("Ticker (or blank to cancel): ").strip().upper()
    if not ticker:
        return None
    if ticker not in companies:
        print("Unknown ticker.")
        return None
    return ticker


def prompt_positive_int(prompt: str) -> int | None:
    raw = input(prompt).strip()
    if not raw:
        return None
    if not raw.isdigit():
        print("Please enter a whole number.")
        return None
    return int(raw)


def handle_buy(portfolio: Dict[str, int], cash: float, companies: Dict[str, Company]) -> float:
    ticker = prompt_ticker(companies)
    if not ticker:
        return cash
    shares = prompt_positive_int("How many shares? ")
    if shares is None:
        return cash
    company = companies[ticker]
    cost = shares * company.price
    if cost > cash:
        print("Not enough cash.")
        return cash
    portfolio[ticker] = portfolio.get(ticker, 0) + shares
    cash -= cost
    print(f"Bought {shares} sh of {ticker} for {format_currency(cost)}")
    return cash


def handle_sell(portfolio: Dict[str, int], cash: float, companies: Dict[str, Company]) -> float:
    ticker = prompt_ticker(companies)
    if not ticker:
        return cash
    if ticker not in portfolio or portfolio[ticker] <= 0:
        print("You do not own that ticker.")
        return cash
    shares_owned = portfolio[ticker]
    shares = prompt_positive_int(f"How many to sell (max {shares_owned})? ")
    if shares is None:
        return cash
    shares = min(shares, shares_owned)
    company = companies[ticker]
    proceeds = shares * company.price
    portfolio[ticker] -= shares
    if portfolio[ticker] == 0:
        del portfolio[ticker]
    cash += proceeds
    print(f"Sold {shares} sh of {ticker} for {format_currency(proceeds)}")
    return cash


def weekly_recap(headlines: List[str], movers: List[Company]) -> None:
    print("\n=== Weekly News ===")
    for line in headlines:
        print(f"- {line}")
    print("\nTop Movers:")
    top = movers[:5]
    for company in top:
        change = company.weekly_change * 100
        bar = pixel_bar(change)
        print(f"{company.ticker:<6} {company.price:>7.2f}  {change:+6.1f}% {bar}  {company.trait}")


def pixel_bar(change_pct: float, width: int = 16) -> str:
    clamped = max(min(change_pct / 25, 1), -1)
    filled = int((clamped + 1) / 2 * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar


def main() -> None:
    random.seed()
    companies = generate_companies()
    company_lookup = {c.ticker: c for c in companies}

    portfolio: Dict[str, int] = {}
    cash = 25_000.0
    goal = 1_000_000.0
    week = 1
    last_theme: str | None = None

    print(PIXEL_BANNER)
    print("Welcome to Trade Raider! Start with $25k and race to $1MM.")
    print("Each turn: peek at the market, buy/sell, then advance a week to see news-driven swings.\n")

    while True:
        weekly_theme = pick_weekly_theme(last_theme)
        last_theme = weekly_theme
        display_market(companies, weekly_theme)
        display_portfolio(portfolio, cash, company_lookup)
        print("\nOptions: (B)uy  (S)ell  (A)dvance week  (Q)uit")
        choice = input("> ").strip().lower()
        if choice == "b":
            cash = handle_buy(portfolio, cash, company_lookup)
            continue
        if choice == "s":
            cash = handle_sell(portfolio, cash, company_lookup)
            continue
        if choice == "q":
            print("Thanks for playing! Come back for another market mood.")
            break
        if choice != "a":
            print("Unknown option, try again.")
            continue

        headlines, movers = apply_weekly_changes(companies, weekly_theme)
        weekly_recap(headlines, movers)
        display_portfolio(portfolio, cash, company_lookup)

        net_worth = cash + sum(
            shares * company_lookup[ticker].price for ticker, shares in portfolio.items()
        )
        print(f"Week {week} ends with net worth {format_currency(net_worth)}\n")
        if net_worth >= goal:
            print("🏆 You smashed the $1MM milestone! Pixel champagne for everyone.")
            break
        week += 1


def description() -> str:
    return textwrap.dedent(
        """
        Trade Raider is a cozy, pixel-flavored stock sandbox. It spins up 125 fictional
        companies with rotating traits so every run feels fresh. Start with $25k,
        trade weekly, react to the headlines, and see if you can ride the hype cycles
        to $1MM. Play straight from the terminal with no dependencies beyond Python 3.
        """
    ).strip()


if __name__ == "__main__":
    main()
