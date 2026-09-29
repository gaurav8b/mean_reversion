# =============================================================================
# DEMO or LIVE
# Mar: H, Jun: M, Sep: U, Dec: Z
# Jan: F, Feb: G, Mar: H, Apr: J, May: K, Jun: M, Jul: N, Aug: Q, Sep: U, Oct: V, Nov: X, Dec: Z
# =============================================================================

ENV    = "DEMO"
SYMBOL = "QQQ"
BROKER_SYMBOL_LONG  = "MNQH6"
BROKER_SYMBOL_SHORT = "MNQM6"

ANCHOR_VWAP_RULES = [
    {
        "id": "PAIR_1",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": 0.0},
        "exit":  {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": 1.0},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_2",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": -1.0},
        "exit":  {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": 1.0},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_3",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": 1.0},
        "exit":  {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": -1.0},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_4",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2025-04-07 09:30:00", "stddev_offset": 1.20},
        "exit":  {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": 0.0},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_5",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2025-06-03 09:30:00", "stddev_offset": -0.50},
        "exit":  {"anchor_time_est": "2025-06-03 09:30:00", "stddev_offset": 1.00},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_6",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2025-04-07 09:30:00", "stddev_offset": 1.80},
        "exit":  {"anchor_time_est": "2025-04-07 09:30:00", "stddev_offset": 0.50},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_7",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2025-04-07 09:30:00", "stddev_offset": 0.5},
        "exit":  {"anchor_time_est": "2025-04-07 09:30:00", "stddev_offset": 1.0},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_8",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-02-05 09:30:00", "stddev_offset": 1.0},
        "exit":  {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": 0.0},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_9",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": 0.0},
        "exit": {"anchor_time_est": "2026-02-05 09:30:00", "stddev_offset": 1.0},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_10",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": -0.2},
        "exit":  {"anchor_time_est": "2025-11-21 09:30:00", "stddev_offset": -0.9},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_11",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-02-05 09:30:00", "stddev_offset": -0.9},
        "exit":  {"anchor_time_est": "2026-01-28 09:30:00", "stddev_offset": 0.0},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "PAIR_12",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2026-02-12 11:00:00", "stddev_offset": 1.0},
        "exit":  {"anchor_time_est": "2026-02-12 11:00:00", "stddev_offset": -1.0},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_13",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2020-03-23 9:30:00", "stddev_offset": 2.0},
        "exit":  {"anchor_time_est": "2020-03-23 9:30:00", "stddev_offset": 0.0},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_14",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2025-11-21 9:30:00", "stddev_offset": -1.1},
        "exit":  {"anchor_time_est": "2026-02-17 9:30:00", "stddev_offset": 0.1},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_15",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-02-17 9:30:00", "stddev_offset": 0.1},
        "exit":  {"anchor_time_est": "2025-11-21 9:30:00", "stddev_offset": -1.1},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_16",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-02-25 9:30:00", "stddev_offset": 0.1},
        "exit":  {"anchor_time_est": "2026-02-25 9:30:00", "stddev_offset": 0.9},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_17",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2026-02-26 9:30:00", "stddev_offset": -0.2},
        "exit":  {"anchor_time_est": "2026-02-26 9:30:00", "stddev_offset": -1.0},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_18",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-02-26 9:30:00", "stddev_offset": -0.8},
        "exit":  {"anchor_time_est": "2026-02-26 9:30:00", "stddev_offset": 0.0},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_19",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2026-02-17 9:30:00", "stddev_offset": -0.1},
        "exit":  {"anchor_time_est": "2026-02-17 9:30:00", "stddev_offset": -0.9},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_20",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-03-02 9:30:00", "stddev_offset": 0.1},
        "exit":  {"anchor_time_est": "2026-02-26 9:30:00", "stddev_offset": 0.9},
        "minimum_pnl_target": 1.0
    },

    {
        "id": "PAIR_21",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2025-11-21 9:30:00", "stddev_offset": -0.5},
        "exit":  {"anchor_time_est": "2026-02-17 9:30:00", "stddev_offset": -0.9},
        "minimum_pnl_target": 1.0
    },

    {
        "id": "PAIR_22",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2026-01-26 9:30:00", "stddev_offset": -1.1},
        "exit":  {"anchor_time_est": "2026-01-26 9:30:00", "stddev_offset": -1.9},
        "minimum_pnl_target": 1.0
    },

    {
        "id": "PAIR_23",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2026-01-26 9:30:00", "stddev_offset": -0.1},
        "exit":  {"anchor_time_est": "2026-02-17 9:30:00", "stddev_offset": -0.9},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_24",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-03-05 9:30:00", "stddev_offset": -0.9},
        "exit":  {"anchor_time_est": "2026-03-05 9:30:00", "stddev_offset": -0.1},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_25",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2025-11-21 9:30:00", "stddev_offset": -0.2},
        "exit":  {"anchor_time_est": "2025-11-21 9:30:00", "stddev_offset": -0.9},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "PAIR_24",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-03-09 04:00:00", "stddev_offset": 0.2},
        "exit":  {"anchor_time_est": "2026-03-09 04:00:00", "stddev_offset": 0.9},
        "minimum_pnl_target": 1.0
    },

    {
        "id": "SPY_PAIR_25",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2026-03-09 04:00:00", "stddev_offset": 0.9},
        "exit":  {"anchor_time_est": "2026-03-09 04:00:00", "stddev_offset": 0.1},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "SPY_PAIR_26",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-03-09 04:00:00", "stddev_offset": 0.1},
        "exit":  {"anchor_time_est": "2026-03-09 04:00:00", "stddev_offset": 0.9},
        "minimum_pnl_target": 2.0
    },
    {
        "id": "SPY_PAIR_27",
        "direction": "LONG",
        "entry": {"anchor_time_est": "2026-02-05 09:30:00", "stddev_offset": -0.9},
        "exit":  {"anchor_time_est": "2026-02-05 09:30:00", "stddev_offset": -0.1},
        "minimum_pnl_target": 1.0
    },
    {
        "id": "SPY_PAIR_28",
        "direction": "SHORT",
        "entry": {"anchor_time_est": "2026-02-05 09:30:00", "stddev_offset": -0.1},
        "exit":  {"anchor_time_est": "2026-02-05 09:30:00", "stddev_offset": -0.9},
        "minimum_pnl_target": 1.0
    },

]

# =============================================================================
# TRADINGBOT — Trend System (LIVE / PRODUCTION)
# =============================================================================

import os, sys, json, time, pytz, signal
import numpy as np
from loguru import logger
from datetime import datetime, timedelta, timezone

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockLatestTradeRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed

export_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if export_path not in sys.path: sys.path.insert(0, export_path)
from tradovate.signal_processor import tradesignal

tz_utc = timezone.utc
tz_est = pytz.timezone("US/Eastern")

# =============================================================================
# CONFIGURATION
# =============================================================================

ALPACA_API_KEY = "YOUR_ALPACA_API_KEY"
ALPACA_SECRET_KEY = "YOUR_ALPACA_SECRET_KEY"

BROKER_ORDER_SIZE_LONG = 1
BROKER_ORDER_SIZE_SHORT = 1

SEND_BROKER_ORDERS = True

LOG_DISPLAY_FREQUENCY_MINUTES = 5
HEARTBEAT_FREQUENCY_MINUTES = 2

MAX_POSITIONS_PER_DIRECTION = 3

# =============================================================================
# RESTRICTED HOURS (EST)
# During these EST hours:
# - No new trades will be opened
# - No existing trades will be closed
# =============================================================================

RESTRICTED_HOURS_EST = [0,1,2,3,4,5,6,7,8,16,17,18,19,20,21,22,23,24]

def is_restricted_hour_est() -> bool:
    now_est = datetime.now(tz_est)
    return now_est.hour in RESTRICTED_HOURS_EST

# =============================================================================
# MINIMUM DISTANCE BETWEEN SAME-DIRECTION POSITIONS
# =============================================================================

MIN_DISTANCE_BETWEEN_LONGS  = 4.0
MIN_DISTANCE_BETWEEN_SHORTS = 4.0

ENABLE_SPURIOUS_CHECK_AGGREGATED = False
ENABLE_SPURIOUS_CHECK_LIVE = False

LIVE_PRICE_BUFFER_SIZE = 5
LIVE_PRICE_OUTLIER_FACTOR = 3.0

# =============================================================================
# AGREED FIX — VWAP CACHE / RECOMPUTE CONTROL
# =============================================================================

VWAP_RECOMPUTE_INTERVAL_SECONDS = 60
ANCHOR_VWAP_CACHE = {}
BARS_API_FAILURES = 0
previous_price = None

MANUAL_TRADES = []

# =============================================================================
# PATHS
# =============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

TRADE_LOG_FILE     = os.path.join(LOGS_DIR, "trade_log.json")
LIVE_STATUS_FILE   = os.path.join(LOGS_DIR, "live_status.json")
CURRENT_PRICE_FILE = os.path.join(LOGS_DIR, "current_price.json")
OPENED_TRADES_FILE = os.path.join(LOGS_DIR, "opened_trades.json")
STATISTICS_FILE    = os.path.join(LOGS_DIR, "statistics.json")
LOG_FILE           = os.path.join(LOGS_DIR, "trading_bot.log")
INTERNALS_FILE     = os.path.join(LOGS_DIR, "internals.json")

# =============================================================================
# LOGGING
# =============================================================================

logger.remove()
logger.add(
    LOG_FILE,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="10 days"
)
logger.add(sys.stderr, level="INFO")

# =============================================================================
# GLOBAL STATE
# =============================================================================

client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)

open_positions = []
last_log_times = {}
live_price_buffer = []

manual_trade_state = {m["id"]: {"open": False} for m in MANUAL_TRADES}

# =============================================================================
# TIME HELPERS
# =============================================================================

def est_to_utc(est_str: str) -> datetime:
    return tz_est.localize(datetime.strptime(est_str, "%Y-%m-%d %H:%M:%S")).astimezone(tz_utc)

def est_now_str() -> str:
    return datetime.now(tz_est).strftime("%Y-%m-%d %H:%M:%S")

# =============================================================================
# JSON UTILITIES
# =============================================================================

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())

def read_json(path, default=None):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        if path in (TRADE_LOG_FILE, OPENED_TRADES_FILE):
            return []
        if path == STATISTICS_FILE:
            return init_statistics_template()
        return {}
    except Exception as e:
        logger.error(f"Read JSON error {path}: {e}")
        return default

# =============================================================================
# POSITION COUNTING
# =============================================================================

def count_open_positions_by_direction(direction: str) -> int:
    return sum(
        1 for pos in open_positions
        if pos.get("status") == "OPEN" and pos.get("position") == direction
    )

# =============================================================================
# MIN DISTANCE FILTER
# =============================================================================

def respects_min_distance(direction: str, price: float) -> bool:
    if direction == "LONG":
        min_distance = MIN_DISTANCE_BETWEEN_LONGS
    else:
        min_distance = MIN_DISTANCE_BETWEEN_SHORTS

    for pos in open_positions:
        if pos.get("status") != "OPEN":
            continue
        if pos.get("position") != direction:
            continue
        if abs(price - float(pos.get("entry_price", 0.0))) < min_distance:
            return False

    return True

# =============================================================================
# STATISTICS
# =============================================================================

def init_statistics_template():
    return {
        "trade_counts_per_hour": {f"{h:02d}": 0 for h in range(24)},
        "largest_winner": 0.0,
        "largest_loser": 0.0,
        "total_trades": 0,
        "winning_trades": 0,
        "win_rate": 0.0,
        "sum_positive_pnl": 0.0,
        "sum_negative_pnl": 0.0,
        "profit_factor": 0.0,
        "sum_trade_durations": 0.0,
        "avg_hold_time_seconds": 0.0,
        "last_closed_trade_time": None
    }

def update_statistics_for_closed_trade(trade):
    stats = read_json(STATISTICS_FILE)
    pnl = float(trade["pnl"])

    stats["total_trades"] += 1

    if pnl > 0:
        stats["winning_trades"] += 1
        stats["sum_positive_pnl"] += pnl
        stats["largest_winner"] = max(stats["largest_winner"], pnl)
    else:
        stats["sum_negative_pnl"] += pnl
        stats["largest_loser"] = min(stats["largest_loser"], pnl)

    if stats["sum_negative_pnl"] != 0:
        stats["profit_factor"] = stats["sum_positive_pnl"] / abs(stats["sum_negative_pnl"])

    stats["win_rate"] = (stats["winning_trades"] / stats["total_trades"]) * 100.0

    if trade.get("entry_time") and trade.get("exit_time"):
        entry = datetime.strptime(trade["entry_time"], "%Y-%m-%d %H:%M:%S")
        exit_ = datetime.strptime(trade["exit_time"], "%Y-%m-%d %H:%M:%S")
        stats["sum_trade_durations"] += (exit_ - entry).total_seconds()
        stats["avg_hold_time_seconds"] = stats["sum_trade_durations"] / stats["total_trades"]

    stats["last_closed_trade_time"] = trade.get("exit_time")
    write_json(STATISTICS_FILE, stats)

# =============================================================================
# LOGGING HELPERS
# =============================================================================

def log_message_throttled(message, key):
    now = datetime.now(tz_utc)
    last = last_log_times.get(key)
    if last is None or (now - last).total_seconds() > LOG_DISPLAY_FREQUENCY_MINUTES * 60:
        logger.info(message)
        last_log_times[key] = now

def log_heartbeat():
    logger.info("Heartbeat: bot running")

# =============================================================================
# SPURIOUS DATA FILTERS
# =============================================================================

def filter_spurious_aggregated(prices, volumes):
    if not ENABLE_SPURIOUS_CHECK_AGGREGATED or len(prices) < 5:
        return prices, volumes
    mean = np.mean(prices)
    std = np.std(prices)
    if std == 0:
        return prices, volumes
    filtered = [(p, v) for p, v in zip(prices, volumes) if abs(p - mean) <= 3 * std]
    if len(filtered) < 2:
        return prices, volumes
    return zip(*filtered)

def filter_live_price(price):
    live_price_buffer.append(price)
    if len(live_price_buffer) > LIVE_PRICE_BUFFER_SIZE:
        live_price_buffer.pop(0)
    if not ENABLE_SPURIOUS_CHECK_LIVE or len(live_price_buffer) < 3:
        return price
    mean = np.mean(live_price_buffer)
    std = np.std(live_price_buffer)
    if std > 0 and abs(price - mean) > LIVE_PRICE_OUTLIER_FACTOR * std:
        logger.warning(f"Ignoring spurious live price: {price}")
        return None
    return price

# =============================================================================
# MARKET DATA
# =============================================================================

def fetch_price_volume_data(start_utc, end_utc):
    global BARS_API_FAILURES

    request = StockBarsRequest(
        symbol_or_symbols=SYMBOL,
        timeframe=TimeFrame.Minute,
        start=start_utc,
        end=end_utc,
        feed=DataFeed.IEX
    )

    try:
        bars = client.get_stock_bars(request)
        BARS_API_FAILURES = 0
    except Exception:
        BARS_API_FAILURES += 1
        time.sleep(min(60, 5 * BARS_API_FAILURES))
        return [], []

    if SYMBOL not in bars.data:
        return [], []

    prices = [bar.close for bar in bars.data[SYMBOL]]
    volumes = [bar.volume for bar in bars.data[SYMBOL]]
    return prices, volumes

def compute_anchored_vwap(anchor_utc):
    now = datetime.now(tz_utc)
    cached = ANCHOR_VWAP_CACHE.get(anchor_utc)

    if cached and (now - cached["ts"]).total_seconds() < VWAP_RECOMPUTE_INTERVAL_SECONDS:
        return cached["vwap"], cached["std"]

    prices, volumes = fetch_price_volume_data(anchor_utc, now)
    prices, volumes = filter_spurious_aggregated(prices, volumes)

    if len(prices) < 2:
        return None, None

    vwap = np.average(prices, weights=volumes)
    std = np.std(prices)

    ANCHOR_VWAP_CACHE[anchor_utc] = {"vwap": vwap, "std": std, "ts": now}
    return vwap, std

# =============================================================================
# BROKER DISPATCH
# =============================================================================

def send_trade_signal(direction, action, qty):
    symbol = BROKER_SYMBOL_LONG if direction == "long" else BROKER_SYMBOL_SHORT
    if SEND_BROKER_ORDERS:
        tradesignal(ENV, symbol, direction, action, qty)
    logger.info(f"Broker signal: {direction.upper()} {action.upper()} {symbol} x{qty}")

# =============================================================================
# GRACEFUL SHUTDOWN
# =============================================================================

def graceful_shutdown(signum, frame):
    logger.info("Shutdown signal received. Exiting cleanly.")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

# =============================================================================
# BOOTSTRAP FILES
# =============================================================================

def bootstrap_files():
    if not os.path.exists(TRADE_LOG_FILE):
        write_json(TRADE_LOG_FILE, [])
    if not os.path.exists(OPENED_TRADES_FILE):
        write_json(OPENED_TRADES_FILE, [])
    if not os.path.exists(LIVE_STATUS_FILE):
        write_json(LIVE_STATUS_FILE, {"current_position": None, "cumulative_pnl": 0.0})
    if not os.path.exists(CURRENT_PRICE_FILE):
        write_json(CURRENT_PRICE_FILE, {"current_price": None})
    if not os.path.exists(STATISTICS_FILE):
        write_json(STATISTICS_FILE, init_statistics_template())

# =============================================================================
# RESTORE OPEN POSITIONS
# =============================================================================

def initialize_open_positions():
    global open_positions, manual_trade_state
    data = read_json(OPENED_TRADES_FILE,default=[])
    open_positions = [t for t in data if t.get("status") == "OPEN"]

    for pos in open_positions:
        if pos.get("manual") and pos.get("manual_id") in manual_trade_state:
            manual_trade_state[pos["manual_id"]]["open"] = True

    long_pos = sum(1 for pos in open_positions if pos["position"] == "LONG")
    short_pos = sum(1 for pos in open_positions if pos["position"] == "SHORT")

    logger.info(f"Restored {len(open_positions)} open position(s) - Long: {long_pos}, Short: {short_pos}")

# =============================================================================
# MANUAL TRADES LOGIC
# =============================================================================

def process_manual_trades(price):
    for m in MANUAL_TRADES:
        mid = m["id"]
        direction = m["direction"].upper()
        entry_price = float(m["entry_price"])
        exit_price = float(m["exit_price"])

        if manual_trade_state[mid]["open"]:
            continue

        if count_open_positions_by_direction(direction) >= MAX_POSITIONS_PER_DIRECTION:
            continue

        if not respects_min_distance(direction, price):
            continue

        trigger = price <= entry_price if direction == "LONG" else price >= entry_price
        if not trigger:
            continue

        size = BROKER_ORDER_SIZE_LONG if direction == "LONG" else BROKER_ORDER_SIZE_SHORT

        pos = {
            "manual": True,
            "manual_id": mid,
            "position": direction,
            "entry_price": price,
            "entry_time": est_now_str(),
            "status": "OPEN",
            "size": size,
            "manual_exit_price": exit_price
        }

        open_positions.append(pos)
        write_json(OPENED_TRADES_FILE, open_positions)

        send_trade_signal(direction.lower(), "buy" if direction == "LONG" else "sell", size)
        manual_trade_state[mid]["open"] = True

# =============================================================================
# HELPER — CHECK IF PAIR IS ALREADY OPEN
# =============================================================================

def is_pair_open(pair_id):
    return any(p for p in open_positions if p.get("pair_id") == pair_id and p.get("status") == "OPEN")

# =============================================================================
# ANCHORED VWAP ENTRY LOGIC
# =============================================================================

def process_anchor_vwap_entries(price):
    for rule in ANCHOR_VWAP_RULES:
        if is_pair_open(rule["id"]):
            continue

        direction = rule["direction"].upper()
        if count_open_positions_by_direction(direction) >= MAX_POSITIONS_PER_DIRECTION:
            continue

        if not respects_min_distance(direction, price):
            continue

        entry_anchor_utc = est_to_utc(rule["entry"]["anchor_time_est"])
        entry_vwap, entry_std = compute_anchored_vwap(entry_anchor_utc)
        if entry_vwap is None:
            continue

        entry_level = entry_vwap + rule["entry"]["stddev_offset"] * entry_std
        if direction == "LONG" and price > entry_level:
            continue
        if direction == "SHORT" and price < entry_level:
            continue

        ##################################################

        prev_price = previous_price
        if prev_price is None:
            continue

        band = 2.0  # allowed distance from entry_level

        if direction == "LONG":
            #crossed_down = (prev_price > entry_level) and (price <= entry_level)
            within_band = price >= (entry_level - band)
            #if not (crossed_down and within_band):
            if not (within_band):
                continue

        elif direction == "SHORT":
            #crossed_up = (prev_price < entry_level) and (price >= entry_level)
            within_band = price <= (entry_level + band)
            #if not (crossed_up and within_band):
            if not (within_band):
                continue

        ##################################################


        exit_anchor_utc = est_to_utc(rule["exit"]["anchor_time_est"])
        exit_vwap, exit_std = compute_anchored_vwap(exit_anchor_utc)
        if exit_vwap is None:
            continue

        exit_level = exit_vwap + rule["exit"]["stddev_offset"] * exit_std
        potential_pnl = (exit_level - price) if direction == "LONG" else (price - exit_level)
        if potential_pnl < rule["minimum_pnl_target"]:
            continue

        size = BROKER_ORDER_SIZE_LONG if direction == "LONG" else BROKER_ORDER_SIZE_SHORT

        pos = {
            "pair_id": rule["id"],
            "manual": False,
            "position": direction,
            "entry_price": price,
            "entry_time": est_now_str(),
            "status": "OPEN",
            "size": size,
            "entry_anchor": rule["entry"]["anchor_time_est"],
            "exit_anchor": rule["exit"]["anchor_time_est"],
            "entry_offset": rule["entry"]["stddev_offset"],
            "exit_offset": rule["exit"]["stddev_offset"],
            "minimum_pnl_target": rule["minimum_pnl_target"]
        }

        open_positions.append(pos)
        write_json(OPENED_TRADES_FILE, open_positions)
        send_trade_signal(direction.lower(), "buy" if direction == "LONG" else "sell", size)

# =============================================================================
# ANCHORED VWAP EXIT LOGIC
# =============================================================================

def process_exits(price):
    closed_positions = []

    for pos in open_positions:
        if pos["status"] != "OPEN":
            continue

        if pos.get("manual"):
            hit = price >= pos["manual_exit_price"] if pos["position"] == "LONG" else price <= pos["manual_exit_price"]
            if hit:
                pnl = price - pos["entry_price"] if pos["position"] == "LONG" else pos["entry_price"] - price
                pos.update({"status": "CLOSED", "exit_price": price, "exit_time": est_now_str(), "pnl": pnl})
                manual_trade_state[pos["manual_id"]]["open"] = False
                closed_positions.append(pos)
            continue

        exit_anchor_utc = est_to_utc(pos["exit_anchor"])
        vwap, std = compute_anchored_vwap(exit_anchor_utc)
        if vwap is None:
            continue

        exit_level = vwap + pos["exit_offset"] * std
        pnl = price - pos["entry_price"] if pos["position"] == "LONG" else pos["entry_price"] - price
        hit = price >= exit_level if pos["position"] == "LONG" else price <= exit_level

        if hit and pnl >= pos["minimum_pnl_target"]:
            pos.update({"status": "CLOSED", "exit_price": price, "exit_time": est_now_str(), "pnl": pnl})
            closed_positions.append(pos)

    if not closed_positions:
        return

    for pos in closed_positions:
        send_trade_signal(pos["position"].lower(), "sell" if pos["position"] == "LONG" else "buy", pos["size"])
        update_statistics_for_closed_trade(pos)

    trade_log = read_json(TRADE_LOG_FILE)
    trade_log.extend(closed_positions)
    write_json(TRADE_LOG_FILE, trade_log)

    open_positions[:] = [p for p in open_positions if p["status"] == "OPEN"]
    write_json(OPENED_TRADES_FILE, open_positions)

# =============================================================================
# MAIN TRADING LOOP
# =============================================================================

def run_trading_bot():
    bootstrap_files()
    initialize_open_positions()

    logger.info("TradingBot started — Anchored VWAP mode active")

    last_heartbeat = datetime.now(tz_utc)

    while True:
        try:
            if (datetime.now(tz_utc) - last_heartbeat).total_seconds() >= HEARTBEAT_FREQUENCY_MINUTES * 60:
                log_heartbeat()
                last_heartbeat = datetime.now(tz_utc)

            req = StockLatestTradeRequest(symbol_or_symbols=SYMBOL)
            trades = client.get_stock_latest_trade(req)

            if SYMBOL not in trades:
                time.sleep(5)
                continue

            raw_price = trades[SYMBOL].price
            price = filter_live_price(raw_price)

            if price is None:
                time.sleep(5)
                continue

            ##################################################

            #previous_price = price
            # previous_price updated at end of loop

            ##################################################

            write_json(CURRENT_PRICE_FILE, {"current_price": price})
            log_message_throttled(f"Live price: {price}", "price")

            if not is_restricted_hour_est():
                process_exits(price)
                process_anchor_vwap_entries(price)
                process_manual_trades(price)
            else:
                log_message_throttled("Restricted EST hour — trading paused", "restricted_hour")
            ##################################################
            global previous_price
            previous_price = price
            ##################################################

            time.sleep(5)

        except Exception as e:
            logger.exception(f"Unexpected runtime error: {e}")
            time.sleep(5)

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    run_trading_bot()