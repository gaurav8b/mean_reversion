import io
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# USER PARAMETERS — edit only these values
# ---------------------------------------------------------------------------
INITIAL_CAPITAL = 100_000.0
CHANNEL_LENGTH = 10
ATR_LENGTH = 20
RISK_FRACTION = 0.01
MAX_GAP_DAYS = 14


def upload_daily_data():
    """Ask the Colab user for exactly one daily CSV file."""
    from google.colab import files

    uploaded = files.upload()
    if len(uploaded) != 1:
        raise ValueError("Please upload exactly one CSV file.")

    filename = next(iter(uploaded))
    return pd.read_csv(io.BytesIO(uploaded[filename])), filename


def prepare_data(raw):
    """Validate the essential columns and create causal indicators."""
    data = raw.copy()
    data.columns = data.columns.str.strip().str.lower()

    required = {"timestamp_est", "open", "high", "low", "close"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    data["timestamp_est"] = pd.to_datetime(
        data["timestamp_est"], utc=True, errors="coerce"
    )
    for column in ["open", "high", "low", "close"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    if data[["timestamp_est", "open", "high", "low", "close"]].isna().any().any():
        raise ValueError("The timestamp or an OHLC column contains an invalid value.")

    data = data.sort_values("timestamp_est").reset_index(drop=True)
    if data["timestamp_est"].duplicated().any():
        raise ValueError("Duplicate timestamps were found.")

    bad_high = data["high"] < data[["open", "close", "low"]].max(axis=1)
    bad_low = data["low"] > data[["open", "close", "high"]].min(axis=1)
    if (bad_high | bad_low).any():
        raise ValueError("At least one row has invalid OHLC ordering.")

    # Convert the timestamp back to New York time and keep its local date.
    data["date"] = (
        data["timestamp_est"]
        .dt.tz_convert("America/New_York")
        .dt.tz_localize(None)
        .dt.normalize()
    )


    # continuous block so that a multi-year gap cannot enter a rolling window.
    segment = data["date"].diff().dt.days.gt(MAX_GAP_DAYS).cumsum()
    largest_segment = segment.value_counts().idxmax()
    removed_rows = int((segment != largest_segment).sum())
    data = data.loc[segment == largest_segment].reset_index(drop=True)

    if len(data) < max(CHANNEL_LENGTH, ATR_LENGTH) + 2:
        raise ValueError("The uploaded file does not contain enough continuous rows.")

    channel_closes = data["close"]
    data["prior_low"] = channel_closes.rolling(CHANNEL_LENGTH).min()
    data["prior_high"] = channel_closes.rolling(CHANNEL_LENGTH).max()

    previous_closes = data["close"].shift(1)
    data["true_range"] = pd.concat([
        data["high"] - data["low"],
        (data["high"] - previous_closes).abs(),
        (data["low"] - previous_closes).abs(),
    ], axis=1).max(axis=1)
    data["atr"] = calculate_atr(data, ATR_LENGTH)

    data["entry_condition"] = data["atr"].gt(0) & (data["close"] < data["prior_low"])
    data["exit_condition"] = data["close"] > data["prior_high"]
    return data, removed_rows


def calculate_atr(data, length):
    """Calculate the ATR series used for position sizing."""
    if length < 1:
        raise ValueError("ATR length must be at least 1.")
    month = data["date"].dt.to_period("M")
    return data.groupby(month)["true_range"].transform("mean")


def run_backtest(data):
    """Execute close-derived signals at the following open."""
    data = data.copy()
    data["entry_signal"] = False
    data["exit_signal"] = False

    cash = INITIAL_CAPITAL
    shares = 0
    pending_order = None
    open_trade = None
    trades = []
    equity_rows = []

    for index, row in data.iterrows():
        date = row["date"]
        open_price = float(row["open"])
        close_price = float(row["close"])

        # First execute the order created after the previous trading day's close.
        if pending_order and pending_order["side"] == "buy":
            cash_limit = math.floor(cash / open_price)
            quantity = min(pending_order["desired_shares"], cash_limit)
            if quantity > 0:
                cash -= quantity * open_price
                shares = quantity
                open_trade = {
                    "entry_signal_date": pending_order["signal_date"],
                    "entry_date": date,
                    "entry_price": open_price,
                    "entry_atr": pending_order["atr"],
                    "risk_budget": pending_order["risk_budget"],
                    "desired_shares": pending_order["desired_shares"],
                    "shares": shares,
                    "entry_index": index,
                }
            pending_order = None

        elif pending_order and pending_order["side"] == "sell":
            exit_price = open_price
            cash += shares * exit_price
            pnl = shares * (exit_price - open_trade["entry_price"])
            trades.append({
                **{key: open_trade[key] for key in [
                    "entry_signal_date", "entry_date", "entry_price",
                    "entry_atr", "risk_budget", "desired_shares", "shares"
                ]},
                "exit_signal_date": pending_order["signal_date"],
                "exit_date": date,
                "exit_price": exit_price,
                "holding_bars": index - open_trade["entry_index"],
                "pnl": pnl,
                "trade_return": exit_price / open_trade["entry_price"] - 1,
                "exit_reason": "10-day high",
            })
            shares = 0
            open_trade = None
            pending_order = None

        # Mark the portfolio at today's close before evaluating today's signal.
        equity = cash + shares * close_price

        # The signal is known only after today's close and is filled tomorrow.
        if index < len(data) - 1:
            if shares == 0 and pd.notna(row["atr"]) and row["entry_condition"]:
                risk_budget = equity * RISK_FRACTION
                desired_shares = math.floor(risk_budget / row["atr"])
                pending_order = {
                    "side": "buy",
                    "signal_date": date,
                    "atr": float(row["atr"]),
                    "risk_budget": risk_budget,
                    "desired_shares": desired_shares,
                }
                data.at[index, "entry_signal"] = True

            elif shares > 0 and row["exit_condition"]:
                pending_order = {"side": "sell", "signal_date": date}
                data.at[index, "exit_signal"] = True

        # Close any remaining position on the final close for reporting only.
        if index == len(data) - 1 and shares > 0:
            cash += shares * close_price
            pnl = shares * (close_price - open_trade["entry_price"])
            trades.append({
                **{key: open_trade[key] for key in [
                    "entry_signal_date", "entry_date", "entry_price",
                    "entry_atr", "risk_budget", "desired_shares", "shares"
                ]},
                "exit_signal_date": pd.NaT,
                "exit_date": date,
                "exit_price": close_price,
                "holding_bars": index - open_trade["entry_index"],
                "pnl": pnl,
                "trade_return": close_price / open_trade["entry_price"] - 1,
                "exit_reason": "end of data",
            })
            shares = 0
            open_trade = None
            equity = cash

        equity_rows.append({
            "date": date,
            "close": close_price,
            "cash": cash,
            "shares": shares,
            "equity": equity,
        })

    trades = pd.DataFrame(trades)
    equity = pd.DataFrame(equity_rows)
    equity["daily_return"] = equity["equity"].pct_change().fillna(0)
    equity["drawdown"] = equity["equity"] / equity["equity"].cummax() - 1
    equity["buy_hold"] = INITIAL_CAPITAL * equity["close"] / equity["close"].iloc[0]

    # Two simple accounting invariants catch silent ledger errors.
    if (equity["cash"] < -0.01).any():
        raise RuntimeError("Cash became negative; the no-borrowing rule was violated.")
    if shares != 0:
        raise RuntimeError("The backtest ended with an unclosed position.")

    return data, trades, equity


def calculate_metrics(trades, equity):
    """Calculate a compact set of common performance statistics."""
    start_date = equity["date"].iloc[0]
    end_date = equity["date"].iloc[-1]
    years = (end_date - start_date).days / 365.25
    ending_equity = equity["equity"].iloc[-1]

    pnl = trades["pnl"] if not trades.empty else pd.Series(dtype=float)
    gross_profit = pnl[pnl > 0].sum()
    gross_loss = -pnl[pnl < 0].sum()
    daily_returns = equity["daily_return"].iloc[1:]

    return pd.Series({
        "Starting capital": INITIAL_CAPITAL,
        "Ending equity": ending_equity,
        "Total return": ending_equity / INITIAL_CAPITAL - 1,
        "CAGR": (ending_equity / INITIAL_CAPITAL) ** (1 / years) - 1,
        "Maximum drawdown": equity["drawdown"].min(),
        "Annualized Sharpe": (
            np.sqrt(252) * daily_returns.mean() / daily_returns.std(ddof=1)
        ),
        "Completed trades": len(trades),
        "Winning trades": int((pnl > 0).sum()),
        "Win rate": (pnl > 0).mean(),
        "Average trade P&L": pnl.mean(),
        "Profit factor": gross_profit / gross_loss if gross_loss > 0 else np.nan,
        "Market exposure": (equity["shares"] > 0).mean(),
        "Buy-and-hold return": equity["buy_hold"].iloc[-1] / INITIAL_CAPITAL - 1,
    }, name="value")


def show_results(filename, removed_rows, trades, equity, metrics):
    """Display the data facts, complete trade ledger, metrics, and one chart."""
    print(f"\nFile: {filename}")
    print(f"Period: {equity['date'].iloc[0].date()} to {equity['date'].iloc[-1].date()}")
    print(f"Rows used: {len(equity)} | isolated rows removed: {removed_rows}")

    print("\nCOMPLETED TRADES")
    if trades.empty:
        print("No trades were produced.")
    else:
        print(trades.round(4).to_string(index=False))

    print("\nPERFORMANCE METRICS")
    percentages = {
        "Total return", "CAGR", "Maximum drawdown", "Win rate",
        "Market exposure", "Buy-and-hold return"
    }
    money = {"Starting capital", "Ending equity", "Average trade P&L"}
    counts = {"Completed trades", "Winning trades"}
    for name, value in metrics.items():
        if name in percentages:
            shown = f"{value:.2%}"
        elif name in money:
            shown = f"${value:,.2f}"
        elif name in counts:
            shown = str(int(value))
        else:
            shown = f"{value:.4f}" if isinstance(value, (float, np.floating)) else str(value)
        print(f"{name:<24} {shown}")

    plt.figure(figsize=(12, 6))
    plt.plot(equity["date"], equity["equity"], label="Mean reversion")
    plt.plot(equity["date"], equity["buy_hold"], label="SPY price-only benchmark")
    plt.title("SPY 10-Day Mean Reversion with Causal ATR Sizing")
    plt.xlabel("Date")
    plt.ylabel("Equity ($)")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    raw, filename = upload_daily_data()
    data, removed_rows = prepare_data(raw)
    signals, trades, equity = run_backtest(data)
    metrics = calculate_metrics(trades, equity)
    show_results(filename, removed_rows, trades, equity, metrics)
    return signals, trades, equity, metrics


if __name__ == "__main__":
    signals, trades, equity, metrics = main()