# (Full file) — refactored to support manual trades + original bot unchanged behavior
import os
import sys
import json
import time
import pytz
import signal
import numpy as np
from datetime import datetime, timedelta
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockLatestTradeRequest
from alpaca.data.timeframe import TimeFrame
from loguru import logger
from signal_processor import tradesignal  # Import the tradesignal function
#from alpaca.data.rest import REST
from alpaca_trade_api.rest import REST
from alpaca_trade_api.rest import REST
from alpaca.data.enums import DataFeed


# =============================================================================
# Configuration Constants
# =============================================================================
# Alpaca API credentials (replace with your actual keys)
ALPACA_API_KEY = "YOUR_ALPACA_API_KEY"
ALPACA_SECRET_KEY = "YOUR_ALPACA_SECRET_KEY"

SYMBOL = "QQQ"      # "QQQ"    # "SPY"  # Underlying symbol to trade

# TWO DISTINCT BROKER SYMBOLS:
BROKER_SYMBOL_LONG = "MNQZ5"     # Symbol used for LONG trades
BROKER_SYMBOL_SHORT = "MNQH6"    # Symbol used for SHORT trades

# DIFFERENT ORDER SIZES FOR LONG AND SHORT TRADES:
BROKER_ORDER_SIZE_LONG = 1   # Original user-defined size for LONG
BROKER_ORDER_SIZE_SHORT = 1  # Original user-defined size for SHORT

LOG_DISPLAY_FREQUENCY_MINUTES = 5   # Minutes between repeated logs
HEARTBEAT_FREQUENCY_MINUTES = 10    # Minutes between heartbeat logs

# =============================================================================
# User Configurable Options
# =============================================================================
TRADE_MODE = "both" #"long"      #"both"  #"short"    # "long"  #"both"     #"long"    #"both"               # Options: "long", "short", "both"
EXIT_CRITERIA_TYPE = "stddev"     # "vwap" or "stddev"
EXIT_VWAP_MODE = "fixed"          # "fixed", "dynamic" (only if EXIT_CRITERIA_TYPE == "vwap")
SEND_BROKER_ORDERS = True #False #True         # Whether to actually send broker orders
ENTRY_STD_DEV_MULTIPLIER = 1.5#0.9
EXIT_STD_DEV_MULTIPLIER =  1.5
STDDEV_EXIT_MODE = "fixed"        # "fixed" or "dynamic"
USE_TIME_THRESHOLD = False        # If True, must remain inside a value area for time_threshold seconds before opening a trade

# =============================================================================
# NEW user-specified minimum PnL target
# =============================================================================
MINIMUM_PNL_TARGET = 0.9 # 0.4  0.8 # 0.4# Only open trades if potential PnL >= this value

# =============================================================================
# NEW: Maximum Positions Per Direction (LONG or SHORT)
# =============================================================================
MAX_POSITIONS_PER_DIRECTION = 5 #3 #3  # Limits max open LONG or SHORT positions

# =============================================================================
# NEW: Toggle spurious data checks
# =============================================================================
ENABLE_SPURIOUS_CHECK_AGGREGATED = False #True  # Toggle for aggregated data (VWAP) filtering
ENABLE_SPURIOUS_CHECK_LIVE = False #True        # Toggle for live price filtering

# =============================================================================
# Manual trades configuration
# =============================================================================
# Fill MANUAL_TRADES with dictionaries for manual signals you want the bot to monitor.
# Example:
#MANUAL_TRADES = [
#    {"id": "M155", "direction": "LONG",  "entry_price": 669.30, "exit_price": 671.50},
#    {"id": "M288", "direction": "SHORT", "entry_price": 673.50, "exit_price": 671.50}
#]
#
# Behavior:
# - The bot watches live prices; when price hits the manual trade's entry_price it will ENTER (one instance per id).
# - When price hits the manual trade's exit_price it will EXIT that manual trade.
# - Only one manual trade per id may be open at any given time. After it is closed it may be re-entered on a future trigger.
MANUAL_TRADES = [

    #{"id": "M15500", "direction": "LONG",  "entry_price": 669.30, "exit_price": 671.50},
    #{"id": "M28800", "direction": "SHORT", "entry_price": 673.50, "exit_price": 671.50}

    #{"id": "M80884", "direction": "LONG",  "entry_price": 681.50, "exit_price": 682.50},
    #{"id": "M16068", "direction": "LONG",  "entry_price": 680.50, "exit_price": 681.50},
    #{"id": "M168", "direction": "LONG",  "entry_price": 682.40, "exit_price": 683.50},
    #{"id": "M1648", "direction": "LONG",  "entry_price": 674.00, "exit_price": 675.00},
    #{"id": "M161080", "direction": "SHORT",  "entry_price": 682.50, "exit_price": 681.50}
    #{"id": "M165", "direction": "SHORT",  "entry_price": 660.50, "exit_price": 658.50},
    #{"id": "M168", "direction": "SHORT",  "entry_price": 665.00, "exit_price": 663.00}
    #{"id": "M288", "direction": "LONG",  "entry_price": 657.10, "exit_price": 659.30},
    #{"id": "M298", "direction": "LONG",  "entry_price": 658.50, "exit_price": 660.50},
    #{"id": "M3", "direction": "LONG",  "entry_price": 663.40, "exit_price": 664.40},
    #{"id": "M4", "direction": "LONG",  "entry_price": 662.10, "exit_price": 663.00},
    #{"id": "M2", "direction": "LONG", "entry_price": 670.50, "exit_price": 672.50},
    #{"id": "M3", "direction": "LONG", "entry_price": 661.50, "exit_price": 664.00},
    #{"id": "M4", "direction": "SHORT", "entry_price": 664.00, "exit_price": 661.50}
    #{"id": "M5", "direction": "SHORT", "entry_price": 665.50, "exit_price": 660.40}
    # Put your manual trade dicts here. Leave blank list [] if none.
]

# =============================================================================
# Value Areas Configuration
# =============================================================================
value_areas = [
    {"id": "AREA20", "high": 690.00, "low": 687.50, "time_threshold": 300},
    {"id": "AREA19", "high": 687.50, "low": 685.00, "time_threshold": 300},
    {"id": "AREA18", "high": 685.00, "low": 682.50, "time_threshold": 300},
    {"id": "AREA17", "high": 682.50, "low": 680.00, "time_threshold": 300},
    {"id": "AREA1", "high": 680.00, "low": 677.50, "time_threshold": 300},
    {"id": "AREA2", "high": 677.50, "low": 675.00, "time_threshold": 300},
    {"id": "AREA3", "high": 675.00, "low": 672.50, "time_threshold": 300},
    {"id": "AREA4", "high": 672.50, "low": 670.00, "time_threshold": 300},
    {"id": "AREA5", "high": 670.00, "low": 667.50, "time_threshold": 300},
    {"id": "AREA6", "high": 667.50, "low": 665.00, "time_threshold": 300},
    {"id": "AREA7", "high": 665.00, "low": 662.50, "time_threshold": 300},
    {"id": "AREA8", "high": 662.50, "low": 660.00, "time_threshold": 300},
    {"id": "AREA9", "high": 660.00, "low": 657.50, "time_threshold": 300},
    {"id": "AREA10", "high": 657.50, "low": 655.00, "time_threshold": 300},
    {"id": "AREA11", "high": 655.00, "low": 652.50, "time_threshold": 300},
    {"id": "AREA12", "high": 652.50, "low": 650.00, "time_threshold": 300},
    {"id": "AREA13", "high": 650.00, "low": 647.50, "time_threshold": 300},
    {"id": "AREA14", "high": 647.50, "low": 645.00, "time_threshold": 300},
    {"id": "AREA15", "high": 645.00, "low": 642.50, "time_threshold": 300},
    {"id": "AREA16", "high": 642.50, "low": 640.00, "time_threshold": 300}
]

# =============================================================================
# Define Absolute Paths
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRADE_LOG_FILE = os.path.join(BASE_DIR, "trade_log.json")
LIVE_STATUS_FILE = os.path.join(BASE_DIR, "live_status.json")
CURRENT_PRICE_FILE = os.path.join(BASE_DIR, "current_price.json")
LOG_FILE = os.path.join(BASE_DIR, "trading_bot.log")
OPENED_TRADES_FILE = os.path.join(BASE_DIR, "opened_trades.json")
STATISTICS_FILE = os.path.join(BASE_DIR, "statistics.json")

# =============================================================================
# Logger Configuration
# =============================================================================
logger.remove()
logger.add(
    LOG_FILE,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="10 days",
    compression="zip"
)
logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    enqueue=True
)

# =============================================================================
# Global Variables
# =============================================================================
# Initialize Alpaca client
client = StockHistoricalDataClient(
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY
)

open_positions = []
last_log_times = {}
current_vwap_data = None
value_area_entry_times = {area["id"]: None for area in value_areas}

# Manual trades runtime state: mapping manual_id -> {"open": bool}
manual_trade_state = {m["id"]: {"open": False} for m in MANUAL_TRADES}

# -----------------------------------------------------------------------------
# Dynamic order sizes for balancing logic
# -----------------------------------------------------------------------------
current_broker_order_size_long = BROKER_ORDER_SIZE_LONG
current_broker_order_size_short = BROKER_ORDER_SIZE_SHORT

# =============================================================================
# Non-Trading Hours in EST
# =============================================================================
RESTRICTED_HOURS_EST = [0,1,2,3,4,5,6,7,17,18,19,20,21,22,23,24]  # Non-trading hours ,4,5,6,7

# =============================================================================
# Rolling Buffer for Live Price Filtering
# =============================================================================
live_price_buffer = []
LIVE_PRICE_BUFFER_SIZE = 5       # Number of recent live prices to keep
LIVE_PRICE_OUTLIER_FACTOR = 3.0  # How many standard deviations to consider spurious

def write_json(file_path, data):
    """Write data to a JSON file, handling directories and flush."""
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory for file: {directory}")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        logger.error(f"Error writing to JSON file {file_path}: {e}")

def read_json(file_path):
    """Read data from a JSON file, or return a default structure if missing."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}. Initializing default content.")
        if file_path == STATISTICS_FILE:
            return init_statistics_template()
        elif file_path in [TRADE_LOG_FILE, OPENED_TRADES_FILE]:
            return []
        else:
            return {}
    except Exception as e:
        logger.error(f"Error reading from JSON file {file_path}: {e}")
        if file_path == STATISTICS_FILE:
            return init_statistics_template()
        elif file_path in [TRADE_LOG_FILE, OPENED_TRADES_FILE]:
            return []
        else:
            return {}

def est_time(dt):
    """Convert UTC time to EST for storage/logging."""
    est = pytz.timezone("US/Eastern")
    return dt.astimezone(est).strftime("%Y-%m-%d %H:%M:%S")

def init_statistics_template():
    """Default structure for statistics.json if missing or corrupt."""
    trade_counts_per_hour = {str(h).zfill(2): 0 for h in range(24)}
    value_area_activity = {area["id"]: 0 for area in value_areas}
    longest_delay = {
        "duration_seconds": 0,
        "start_time": "N/A",
        "end_time": "N/A"
    }
    stats_template = {
        "trade_counts_per_hour": trade_counts_per_hour,
        "value_area_activity": value_area_activity,
        "longest_time_between_closings": longest_delay,
        "last_closed_trade_time": None,
        "largest_winner": 0.0,
        "largest_loser": 0.0,
        "total_trades": 0,
        "winning_trades": 0,
        "win_rate": 0.0,
        "sum_positive_pnl": 0.0,
        "sum_negative_pnl": 0.0,
        "profit_factor": 0.0,
        "sum_trade_durations": 0.0,
        "avg_hold_time_seconds": 0.0
    }
    return stats_template

def is_non_trading_hour():
    """Returns True if the current time in EST falls within RESTRICTED_HOURS_EST."""
    est_tz = pytz.timezone("US/Eastern")
    now_est = datetime.now(tz=est_tz)
    return now_est.hour in RESTRICTED_HOURS_EST

def log_message_throttled(message, key="default"):
    """Log a message only if enough time has passed since last log under the same key."""
    global last_log_times
    now = datetime.now()
    frequency_seconds = LOG_DISPLAY_FREQUENCY_MINUTES * 60
    if key not in last_log_times or (now - last_log_times[key]).total_seconds() >= frequency_seconds:
        logger.info(message)
        last_log_times[key] = now

def log_heartbeat():
    """Regular heartbeat message to ensure the bot is running."""
    logger.info("Heartbeat: Trading bot is active and running.")

def count_open_positions():
    """Return the total counts of open LONG vs. SHORT positions."""
    long_count = sum(1 for pos in open_positions if pos["status"] == "OPEN" and pos["position"] == "LONG")
    short_count = sum(1 for pos in open_positions if pos["status"] == "OPEN" and pos["position"] == "SHORT")
    return long_count, short_count

def update_dynamic_order_sizes():
    """
    If the ratio of open positions (larger_count / smaller_count) >= 2,
    double the order size for the lesser side. Once ratio < 2, revert to normal.
    """
    global current_broker_order_size_long, current_broker_order_size_short
    long_count, short_count = count_open_positions()

    # If both sides are zero => revert to original
    if long_count == 0 and short_count == 0:
        current_broker_order_size_long = BROKER_ORDER_SIZE_LONG
        current_broker_order_size_short = BROKER_ORDER_SIZE_SHORT
        return

    # If one side is zero
    if long_count == 0 and short_count >= 2:
        current_broker_order_size_long = BROKER_ORDER_SIZE_LONG * 1 #2
        current_broker_order_size_short = BROKER_ORDER_SIZE_SHORT
        return
    elif short_count == 0 and long_count >= 2:
        current_broker_order_size_long = BROKER_ORDER_SIZE_LONG
        current_broker_order_size_short = BROKER_ORDER_SIZE_SHORT * 1 #2
        return

    # If both > 0, check ratio
    if long_count > 0 and short_count > 0:
        ratio = max(long_count, short_count) / min(long_count, short_count)
        if ratio >= 2:
            if long_count > short_count:
                current_broker_order_size_short = BROKER_ORDER_SIZE_SHORT * 1 #2
                current_broker_order_size_long = BROKER_ORDER_SIZE_LONG
            else:
                current_broker_order_size_long = BROKER_ORDER_SIZE_LONG * 1 #2
                current_broker_order_size_short = BROKER_ORDER_SIZE_SHORT
        else:
            # Revert to original sizes
            current_broker_order_size_long = BROKER_ORDER_SIZE_LONG
            current_broker_order_size_short = BROKER_ORDER_SIZE_SHORT

# =============================================================================
# Spurious Data Filter for Aggregated Data
# =============================================================================
def filter_spurious_data(prices, volumes, threshold_multiplier=3.0):
    """
    Filters out aggregated data points that are spurious (significantly far from the mean).
    Returns filtered prices and volumes. If nearly all points get removed, revert to original.
    """
    # If user toggle is off, skip filtering
    if not ENABLE_SPURIOUS_CHECK_AGGREGATED:
        return prices, volumes

    if len(prices) < 5:
        # If we have too few data points, skip filtering
        return prices, volumes

    mean_price = np.mean(prices)
    std_price = np.std(prices)

    if std_price == 0:
        return prices, volumes

    new_prices = []
    new_volumes = []
    skip_count = 0

    for p, v in zip(prices, volumes):
        if abs(p - mean_price) > threshold_multiplier * std_price:
            skip_count += 1
            continue
        new_prices.append(p)
        new_volumes.append(v)

    if skip_count > 0:
        logger.warning(f"Filtered out {skip_count} spurious aggregated data point(s).")

    if len(new_prices) < 2:
        logger.warning("Filtering removed too many data points, reverting to original dataset.")
        return prices, volumes

    return new_prices, new_volumes

# =============================================================================
# Spurious Check for Live Price
# =============================================================================
def filter_live_price(new_price):
    """
    Returns None if new_price is deemed spurious (based on rolling buffer).
    Otherwise returns new_price.
    """
    global live_price_buffer

    # If user toggle is off, we accept all prices directly
    if not ENABLE_SPURIOUS_CHECK_LIVE:
        live_price_buffer.append(new_price)
        if len(live_price_buffer) > LIVE_PRICE_BUFFER_SIZE:
            live_price_buffer.pop(0)
        return new_price

    # If the buffer is not yet populated, accept the price
    if len(live_price_buffer) < 3:
        live_price_buffer.append(new_price)
        return new_price

    mean_price = np.mean(live_price_buffer)
    std_price = np.std(live_price_buffer)

    if std_price == 0:
        # Accept (no variance in buffer)
        live_price_buffer.append(new_price)
        if len(live_price_buffer) > LIVE_PRICE_BUFFER_SIZE:
            live_price_buffer.pop(0)
        return new_price

    if abs(new_price - mean_price) > LIVE_PRICE_OUTLIER_FACTOR * std_price:
        logger.warning(
            f"Detected spurious live price {new_price:.2f} "
            f"(mean {mean_price:.2f}, std {std_price:.2f}). Ignoring."
        )
        return None

    # Otherwise accept & store
    live_price_buffer.append(new_price)
    if len(live_price_buffer) > LIVE_PRICE_BUFFER_SIZE:
        live_price_buffer.pop(0)
    return new_price

def fetch_price_volume_data(anchor_start, anchor_end):
    """Fetch aggregated price/volume data from Alpaca."""
    try:
        # Create a request for historical bars
        request_params = StockBarsRequest(
            symbol_or_symbols=SYMBOL,
            timeframe=TimeFrame.Minute,
            start=anchor_start,
            end=anchor_end,
            feed=DataFeed.IEX
        )

        # Get the bars
        bars = client.get_stock_bars(request_params)

        # Extract prices and volumes
        if SYMBOL in bars.data:
            bar_data = bars.data[SYMBOL]
            prices = [bar.close for bar in bar_data]
            volumes = [bar.volume for bar in bar_data]
            return prices, volumes
        else:
            return [], []

    except Exception as e:
        logger.error(f"Error fetching data from Alpaca: {e}")
        return [], []

def calculate_vwap_and_bands(prices, volumes):
    """Compute VWAP, std dev, upper/lower bands."""
    if len(prices) < 2:
        return None, None, None, None
    vwap = np.average(prices, weights=volumes)
    std_dev = np.std(prices)
    upper_band = vwap + ENTRY_STD_DEV_MULTIPLIER * std_dev
    lower_band = vwap - ENTRY_STD_DEV_MULTIPLIER * std_dev
    return vwap, upper_band, lower_band, std_dev

def send_trade_signal(position, action, qty=1):
    """
    Single trade with the specified lot-size.
    position: 'long' or 'short'
    action: 'buy' or 'sell'
    qty: how many lots to send in one shot
    """
    global current_broker_order_size_long, current_broker_order_size_short

    broker_symbol = BROKER_SYMBOL_LONG if position == "long" else BROKER_SYMBOL_SHORT

    if SEND_BROKER_ORDERS:
        try:
            tradesignal(broker_symbol, position, action, qty)
            logger.info(f"Trade signal sent: {position} {action} for {broker_symbol} (size={qty}).")
        except Exception as e:
            logger.error(f"Error sending trade signal: {e}")
    else:
        logger.info(f"Trade signal (mock): {position} {action} for {broker_symbol} (size={qty}).")

def graceful_shutdown(signum, frame):
    """Handle SIGINT/SIGTERM for a graceful shutdown."""
    logger.info("Shutdown signal received. Closing trading bot gracefully...")
    sys.exit(0)

def record_opened_trade(position_info):
    opened_trades = read_json(OPENED_TRADES_FILE)
    opened_trades.append(position_info)
    write_json(OPENED_TRADES_FILE, opened_trades)

def update_statistics_for_closed_trade(trade):
    """
    Called when a trade transitions from OPEN to CLOSED.
    """
    statistics = read_json(STATISTICS_FILE)

    exit_time_str = trade.get("exit_time", None)
    entry_time_str = trade.get("entry_time", None)
    pnl = float(trade.get("pnl", 0.0))
    value_area_id = trade.get("value_area_id", None)

    # 1) increment trades/hour
    if exit_time_str:
        exit_dt = datetime.strptime(exit_time_str, "%Y-%m-%d %H:%M:%S")
        hour_str = exit_dt.strftime("%H")
        if hour_str in statistics["trade_counts_per_hour"]:
            statistics["trade_counts_per_hour"][hour_str] += 1

        # gap from last_closed_trade_time
        last_time_str = statistics.get("last_closed_trade_time", None)
        if last_time_str is not None:
            last_time_dt = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
            delta = exit_dt - last_time_dt
            delta_seconds = delta.total_seconds()
            record_seconds = statistics["longest_time_between_closings"]["duration_seconds"]
            if delta_seconds > record_seconds:
                statistics["longest_time_between_closings"]["duration_seconds"] = delta_seconds
                statistics["longest_time_between_closings"]["start_time"] = last_time_str
                statistics["longest_time_between_closings"]["end_time"] = exit_time_str

        statistics["last_closed_trade_time"] = exit_time_str

    # 2) value area activity
    if value_area_id and value_area_id in statistics["value_area_activity"]:
        statistics["value_area_activity"][value_area_id] += 1

    # 3) largest winner/loser
    if pnl > statistics["largest_winner"]:
        statistics["largest_winner"] = pnl
    if pnl < statistics["largest_loser"]:
        statistics["largest_loser"] = pnl

    # 4) total trades, winning trades => win rate
    statistics["total_trades"] += 1
    if pnl > 0:
        statistics["winning_trades"] += 1
    total_trades = statistics["total_trades"]
    wins = statistics["winning_trades"]
    if total_trades > 0:
        statistics["win_rate"] = (wins / total_trades) * 100.0

    # 5) sum of positive/negative PnLs => profit factor
    if pnl > 0:
        statistics["sum_positive_pnl"] += pnl
    elif pnl < 0:
        statistics["sum_negative_pnl"] += pnl
    neg_pnl = statistics["sum_negative_pnl"]
    pos_pnl = statistics["sum_positive_pnl"]
    if neg_pnl != 0:
        statistics["profit_factor"] = pos_pnl / abs(neg_pnl)
    else:
        if pos_pnl > 0:
            statistics["profit_factor"] = float('inf')
        else:
            statistics["profit_factor"] = 0.0

    # 6) average hold time
    if entry_time_str and exit_time_str:
        entry_dt = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
        exit_dt = datetime.strptime(exit_time_str, "%Y-%m-%d %H:%M:%S")
        duration_seconds = (exit_dt - entry_dt).total_seconds()
        statistics["sum_trade_durations"] += duration_seconds
        statistics["avg_hold_time_seconds"] = statistics["sum_trade_durations"] / total_trades

    write_json(STATISTICS_FILE, statistics)

def compute_fixed_exit_threshold(direction, entry_price, vwap, std_dev):
    """Compute the exit threshold based on user-chosen EXIT_CRITERIA_TYPE."""
    if EXIT_CRITERIA_TYPE == "vwap":
        if EXIT_VWAP_MODE == "fixed":
            return vwap
        else:
            return "N/A"
    elif EXIT_CRITERIA_TYPE == "stddev":
        if STDDEV_EXIT_MODE == "fixed":
            if direction == "SHORT":
                return vwap - EXIT_STD_DEV_MULTIPLIER * std_dev
            else:
                return vwap + EXIT_STD_DEV_MULTIPLIER * std_dev
        else:
            return "N/A"
    return "N/A"

def close_positions_if_exit_condition_met(price, latest_vwap, latest_std_dev):
    """Check open trades for exit conditions and close them if triggered."""
    global open_positions, manual_trade_state
    live_status = read_json(LIVE_STATUS_FILE)
    cumulative_pnl = live_status.get("cumulative_pnl", 0)

    # Skip closing if within restricted hours
    if is_non_trading_hour():
        log_message_throttled("Currently in non-trading hours, skipping close position checks.", "non_trading_hours")
        return

    for position in open_positions:
        if position["status"] == "OPEN":
            # Manual positions: use provided target exit_price field
            if position.get("manual", False):
                # For manual SHORT: exit when price <= exit_price
                if position["position"] == "SHORT" and price <= position.get("manual_exit_price"):
                    pnl = position["entry_price"] - price
                    position.update({
                        "status": "CLOSED",
                        "exit_price": price,
                        "exit_time": est_time(datetime.now()),
                        "pnl": pnl
                    })
                    send_trade_signal("short", "buy", qty=position["size"])
                    log_message_throttled(f"Exited MANUAL SHORT {position.get('manual_id')} at {price:.2f}. PnL: {pnl:.2f}", "manual_trade_exit")
                    cumulative_pnl += pnl
                    # mark manual state as closed
                    mid = position.get("manual_id")
                    if mid in manual_trade_state:
                        manual_trade_state[mid]["open"] = False

                # For manual LONG: exit when price >= exit_price
                elif position["position"] == "LONG" and price >= position.get("manual_exit_price"):
                    pnl = price - position["entry_price"]
                    position.update({
                        "status": "CLOSED",
                        "exit_price": price,
                        "exit_time": est_time(datetime.now()),
                        "pnl": pnl
                    })
                    send_trade_signal("long", "sell", qty=position["size"])
                    log_message_throttled(f"Exited MANUAL LONG {position.get('manual_id')} at {price:.2f}. PnL: {pnl:.2f}", "manual_trade_exit")
                    cumulative_pnl += pnl
                    mid = position.get("manual_id")
                    if mid in manual_trade_state:
                        manual_trade_state[mid]["open"] = False

                # continue to next position after manual handling
                continue

            # Non-manual (VWAP) logic remains unchanged
            if EXIT_CRITERIA_TYPE == "vwap":
                exit_threshold = (position["entry_vwap"]
                                  if EXIT_VWAP_MODE == "fixed"
                                  else latest_vwap)
            else:
                entry_vwap = position["entry_vwap"]
                entry_std_dev = position["entry_std_dev"]
                exit_std_dev_multiplier = position["exit_std_dev_multiplier"]

                if STDDEV_EXIT_MODE == "fixed":
                    if position["position"] == "SHORT":
                        exit_threshold = entry_vwap - exit_std_dev_multiplier * entry_std_dev
                    else:
                        exit_threshold = entry_vwap + exit_std_dev_multiplier * entry_std_dev
                else:
                    if position["position"] == "SHORT":
                        exit_threshold = latest_vwap - exit_std_dev_multiplier * latest_std_dev
                    else:
                        exit_threshold = latest_vwap + exit_std_dev_multiplier * latest_std_dev

            # Evaluate exit condition
            if position["position"] == "SHORT" and price <= exit_threshold:
                pnl = position["entry_price"] - price
                position.update({
                    "status": "CLOSED",
                    "exit_price": price,
                    "exit_time": est_time(datetime.now()),
                    "pnl": pnl
                })
                send_trade_signal("short", "buy", qty=position["size"])
                log_message_throttled(f"Exited SHORT at {price:.2f}. PnL: {pnl:.2f}", "trade_exit")
                cumulative_pnl += pnl

            elif position["position"] == "LONG" and price >= exit_threshold:
                pnl = price - position["entry_price"]
                position.update({
                    "status": "CLOSED",
                    "exit_price": price,
                    "exit_time": est_time(datetime.now()),
                    "pnl": pnl
                })
                send_trade_signal("long", "sell", qty=position["size"])
                log_message_throttled(f"Exited LONG at {price:.2f}. PnL: {pnl:.2f}", "trade_exit")
                cumulative_pnl += pnl

    closed_trades = [pos for pos in open_positions if pos["status"] == "CLOSED"]
    open_positions = [pos for pos in open_positions if pos["status"] == "OPEN"]

    # Update live status
    if open_positions:
        live_status.update({
            "current_position": open_positions[0]["position"],
            "entry_price": open_positions[0]["entry_price"],
            "entry_time": open_positions[0]["entry_time"]
        })
    else:
        live_status.update({
            "current_position": None,
            "entry_price": None,
            "entry_time": None
        })

    live_status["cumulative_pnl"] = cumulative_pnl
    write_json(LIVE_STATUS_FILE, live_status)

    if closed_trades:
        trade_log = read_json(TRADE_LOG_FILE)
        trade_log.extend(closed_trades)
        write_json(TRADE_LOG_FILE, trade_log)

        # Reflect closures in opened_trades.json
        opened_trades_data = read_json(OPENED_TRADES_FILE)
        for closed_trade in closed_trades:
            for ot in opened_trades_data:
                if (ot.get("status") == "OPEN"
                    and ot.get("position") == closed_trade["position"]
                    and ot.get("value_area_id") == closed_trade.get("value_area_id")
                    and ot.get("entry_time") == closed_trade["entry_time"]):
                    ot.update(closed_trade)
        write_json(OPENED_TRADES_FILE, opened_trades_data)

        for closed_trade in closed_trades:
            update_statistics_for_closed_trade(closed_trade)

def already_open(direction, area_id):
    """Check if a position in the same direction and value area is already open."""
    for position in open_positions:
        if position["status"] == "OPEN" and position["position"] == direction:
            if position["value_area_id"] == area_id:
                return True
    return False

def open_new_positions(price, vwap, upper_band, lower_band, std_dev):
    """Open new positions in one trade (size = broker_order_size_xxx)."""
    global open_positions, value_area_entry_times
    current_time = datetime.now()

    if is_non_trading_hour():
        log_message_throttled("Currently in non-trading hours, skipping open position checks.", "non_trading_hours")
        return

    for area in value_areas:
        area_id = area["id"]
        area_low = area["low"]
        area_high = area["high"]
        area_threshold = area["time_threshold"]

        # Price inside area?
        if area_low <= price <= area_high:
            if USE_TIME_THRESHOLD:
                # Start or continue counting
                if value_area_entry_times[area_id] is None:
                    value_area_entry_times[area_id] = current_time
                    log_message_throttled(
                        f"Price entered value area {area_id}. Starting timer.",
                        f"value_area_{area_id}"
                    )
                else:
                    elapsed_time = (current_time - value_area_entry_times[area_id]).total_seconds()
                    if elapsed_time >= area_threshold:
                        value_area_entry_times[area_id] = None

                        can_go_short = (TRADE_MODE in ["both", "short"]) and (price > upper_band)
                        can_go_long = (TRADE_MODE in ["both", "long"]) and (price < lower_band)

                        # Check current open count for SHORT before opening a new one
                        if can_go_short and not already_open("SHORT", area_id):
                            short_positions = sum(1 for pos in open_positions
                                                  if pos["status"] == "OPEN" and pos["position"] == "SHORT")
                            if short_positions >= MAX_POSITIONS_PER_DIRECTION:
                                logger.info(f"Reached max short positions. Skipping new short trade in {area_id}.")
                            else:
                                fixed_target_price = compute_fixed_exit_threshold("SHORT", price, vwap, std_dev)
                                potential_pnl = price - fixed_target_price  # SHORT perspective

                                if potential_pnl < MINIMUM_PNL_TARGET:
                                    logger.info(
                                        f"Skipping SHORT in {area_id}; PnL ({potential_pnl:.2f}) < MINIMUM_PNL_TARGET."
                                    )
                                else:
                                    short_size = current_broker_order_size_short
                                    new_short_position = {
                                        "position": "SHORT",
                                        "value_area_id": area_id,
                                        "entry_price": price,
                                        "anchor_price": vwap,
                                        "entry_vwap": vwap,
                                        "entry_std_dev": std_dev,
                                        "exit_std_dev_multiplier": EXIT_STD_DEV_MULTIPLIER,
                                        "status": "OPEN",
                                        "entry_time": est_time(datetime.now()),
                                        "target_price": fixed_target_price,
                                        "size": short_size
                                    }
                                    open_positions.append(new_short_position)
                                    record_opened_trade(new_short_position)
                                    send_trade_signal("short", "sell", qty=short_size)
                                    log_message_throttled(
                                        f"Entered SHORT in {area_id} at {price:.2f} (size={short_size})",
                                        f"trade_entry_{area_id}_short"
                                    )

                        # Check current open count for LONG before opening a new one
                        if can_go_long and not already_open("LONG", area_id):
                            long_positions = sum(1 for pos in open_positions
                                                 if pos["status"] == "OPEN" and pos["position"] == "LONG")
                            if long_positions >= MAX_POSITIONS_PER_DIRECTION:
                                logger.info(f"Reached max long positions. Skipping new long trade in {area_id}.")
                            else:
                                fixed_target_price = compute_fixed_exit_threshold("LONG", price, vwap, std_dev)
                                potential_pnl = fixed_target_price - price  # LONG perspective

                                if potential_pnl < MINIMUM_PNL_TARGET:
                                    logger.info(
                                        f"Skipping LONG in {area_id}; PnL ({potential_pnl:.2f}) < MINIMUM_PNL_TARGET."
                                    )
                                else:
                                    long_size = current_broker_order_size_long
                                    new_long_position = {
                                        "position": "LONG",
                                        "value_area_id": area_id,
                                        "entry_price": price,
                                        "anchor_price": vwap,
                                        "entry_vwap": vwap,
                                        "entry_std_dev": std_dev,
                                        "exit_std_dev_multiplier": EXIT_STD_DEV_MULTIPLIER,
                                        "status": "OPEN",
                                        "entry_time": est_time(datetime.now()),
                                        "target_price": fixed_target_price,
                                        "size": long_size
                                    }
                                    open_positions.append(new_long_position)
                                    record_opened_trade(new_long_position)
                                    send_trade_signal("long", "buy", qty=long_size)
                                    log_message_throttled(
                                        f"Entered LONG in {area_id} at {price:.2f} (size={long_size})",
                                        f"trade_entry_{area_id}_long"
                                    )
            else:
                # Not using time threshold, open immediately
                can_go_short = (TRADE_MODE in ["both", "short"]) and (price > upper_band)
                can_go_long = (TRADE_MODE in ["both", "long"]) and (price < lower_band)

                # Check current open count for SHORT
                if can_go_short and not already_open("SHORT", area_id):
                    short_positions = sum(1 for pos in open_positions
                                          if pos["status"] == "OPEN" and pos["position"] == "SHORT")
                    if short_positions >= MAX_POSITIONS_PER_DIRECTION:
                        logger.info(f"Reached max short positions. Skipping new short trade in {area_id}.")
                    else:
                        fixed_target_price = compute_fixed_exit_threshold("SHORT", price, vwap, std_dev)
                        potential_pnl = price - fixed_target_price
                        if potential_pnl < MINIMUM_PNL_TARGET:
                            logger.info(
                                f"Skipping SHORT in {area_id}; PnL ({potential_pnl:.2f}) < MINIMUM_PNL_TARGET."
                            )
                        else:
                            short_size = current_broker_order_size_short
                            new_short_position = {
                                "position": "SHORT",
                                "value_area_id": area_id,
                                "entry_price": price,
                                "anchor_price": vwap,
                                "entry_vwap": vwap,
                                "entry_std_dev": std_dev,
                                "exit_std_dev_multiplier": EXIT_STD_DEV_MULTIPLIER,
                                "status": "OPEN",
                                "entry_time": est_time(datetime.now()),
                                "target_price": fixed_target_price,
                                "size": short_size
                            }
                            open_positions.append(new_short_position)
                            record_opened_trade(new_short_position)
                            send_trade_signal("short", "sell", qty=short_size)
                            log_message_throttled(
                                f"Entered SHORT in {area_id} at {price:.2f} (size={short_size})",
                                f"trade_entry_{area_id}_short"
                            )

                # Check current open count for LONG
                if can_go_long and not already_open("LONG", area_id):
                    long_positions = sum(1 for pos in open_positions
                                         if pos["status"] == "OPEN" and pos["position"] == "LONG")
                    if long_positions >= MAX_POSITIONS_PER_DIRECTION:
                        logger.info(f"Reached max long positions. Skipping new long trade in {area_id}.")
                    else:
                        fixed_target_price = compute_fixed_exit_threshold("LONG", price, vwap, std_dev)
                        potential_pnl = fixed_target_price - price
                        if potential_pnl < MINIMUM_PNL_TARGET:
                            logger.info(
                                f"Skipping LONG in {area_id}; PnL ({potential_pnl:.2f}) < MINIMUM_PNL_TARGET."
                            )
                        else:
                            long_size = current_broker_order_size_long
                            new_long_position = {
                                "position": "LONG",
                                "value_area_id": area_id,
                                "entry_price": price,
                                "anchor_price": vwap,
                                "entry_vwap": vwap,
                                "entry_std_dev": std_dev,
                                "exit_std_dev_multiplier": EXIT_STD_DEV_MULTIPLIER,
                                "status": "OPEN",
                                "entry_time": est_time(datetime.now()),
                                "target_price": fixed_target_price,
                                "size": long_size
                            }
                            open_positions.append(new_long_position)
                            record_opened_trade(new_long_position)
                            send_trade_signal("long", "buy", qty=long_size)
                            log_message_throttled(
                                f"Entered LONG in {area_id} at {price:.2f} (size={long_size})",
                                f"trade_entry_{area_id}_long"
                            )
        else:
            # If price left the area, reset the timer if it was set
            if value_area_entry_times[area_id] is not None:
                value_area_entry_times[area_id] = None
                log_message_throttled(
                    f"Price exited value area {area_id}. Timer reset.",
                    f"value_area_reset_{area_id}"
                )

# =============================================================================
# Manual trades handling
# =============================================================================
def process_manual_trades(price):
    """
    Monitor and act on MANUAL_TRADES:
    - Enter when live price hits entry_price (with correct limit logic)
    - Exit when live price hits exit_price (handled elsewhere)
    - Only one manual trade per manual id can be open at a time
    """
    global manual_trade_state, open_positions

    if not MANUAL_TRADES:
        return

    if is_non_trading_hour():
        # Keep manual trades dormant during restricted hours as well
        return

    for m in MANUAL_TRADES:
        mid = m["id"]
        direction = m["direction"].upper()
        entry_p = float(m["entry_price"])
        exit_p = float(m["exit_price"])

        # Ensure state exists
        if mid not in manual_trade_state:
            manual_trade_state[mid] = {"open": False}

        # If already open: skip (exit is handled elsewhere)
        if manual_trade_state[mid]["open"]:
            continue

        # Corrected entry trigger logic
        triggered = False
        if direction == "LONG":
            # For LONG, price must be <= entry_price to enter
            if price <= entry_p:
                triggered = True
        elif direction == "SHORT":
            # For SHORT, price must be >= entry_price to enter
            if price >= entry_p:
                triggered = True
        else:
            logger.error(f"Manual trade {mid} has invalid direction: {direction}. Skipping.")
            continue

        if triggered:
            # Respect max positions per direction
            direction_label = "LONG" if direction == "LONG" else "SHORT"
            current_dir_count = sum(1 for pos in open_positions if pos["status"] == "OPEN" and pos["position"] == direction_label)
            if current_dir_count >= MAX_POSITIONS_PER_DIRECTION:
                logger.info(f"Manual trade {mid}: reached max positions for {direction_label}. Skipping entry.")
                continue

            # Create manual position
            size = current_broker_order_size_long if direction == "LONG" else current_broker_order_size_short
            entry_time_str = est_time(datetime.now())

            manual_position = {
                "position": direction_label,
                "value_area_id": None,
                "entry_price": price,
                "anchor_price": None,
                "entry_vwap": current_vwap_data["vwap"] if current_vwap_data else None,
                "entry_std_dev": None,
                "exit_std_dev_multiplier": None,
                "status": "OPEN",
                "entry_time": entry_time_str,
                "target_price": exit_p,
                "size": size,
                # manual-specific fields
                "manual": True,
                "manual_id": mid,
                "manual_entry_price": entry_p,
                "manual_exit_price": exit_p
            }

            open_positions.append(manual_position)
            record_opened_trade(manual_position)

            # Send appropriate broker order
            if direction == "LONG":
                send_trade_signal("long", "buy", qty=size)
                log_message_throttled(f"Entered MANUAL LONG {mid} at {price:.2f} (size={size})", f"manual_entry_{mid}")
            else:
                send_trade_signal("short", "sell", qty=size)
                log_message_throttled(f"Entered MANUAL SHORT {mid} at {price:.2f} (size={size})", f"manual_entry_{mid}")

            manual_trade_state[mid]["open"] = True


def initialize_open_positions():
    """
    Reads 'opened_trades.json' and populates the global open_positions
    with any trades still marked as OPEN from the last session.
    Also restore manual_trade_state for manual trades that are already open.
    """
    global open_positions, manual_trade_state
    opened_trades_data = read_json(OPENED_TRADES_FILE)
    open_positions_in_file = [trade for trade in opened_trades_data if trade.get("status") == "OPEN"]
    open_positions = open_positions_in_file

    # If there are manual positions in the file, mark their manual_id as open
    for pos in open_positions:
        if pos.get("manual") and pos.get("manual_id"):
            mid = pos["manual_id"]
            if mid not in manual_trade_state:
                manual_trade_state[mid] = {"open": True}
            else:
                manual_trade_state[mid]["open"] = True

    if open_positions:
        logger.info(f"Restored {len(open_positions)} OPEN position(s) from previous session.")
    else:
        logger.info("No OPEN positions found from previous session.")

def run_trading_bot():
    global current_vwap_data

    # Initialize JSON files if missing
    if not os.path.exists(TRADE_LOG_FILE):
        write_json(TRADE_LOG_FILE, [])
    if not os.path.exists(LIVE_STATUS_FILE):
        write_json(LIVE_STATUS_FILE, {"current_position": None, "cumulative_pnl": 0})
    if not os.path.exists(CURRENT_PRICE_FILE):
        write_json(CURRENT_PRICE_FILE, {"current_price": 0})
    if not os.path.exists(OPENED_TRADES_FILE):
        write_json(OPENED_TRADES_FILE, [])
    if not os.path.exists(STATISTICS_FILE):
        write_json(STATISTICS_FILE, init_statistics_template())

    # Restore any open positions
    initialize_open_positions()

    logger.info("Trading bot started.")
    last_heartbeat = datetime.now()

    while True:
        try:
            # 1) Update dynamic order sizes
            update_dynamic_order_sizes()

            now = datetime.now()
            anchor_start = now - timedelta(minutes=30) # 15,60,240,1440,60, 10080
            anchor_end = now

            # 2) Fetch aggregated data
            prices, volumes = fetch_price_volume_data(anchor_start, anchor_end)
            if not prices or not volumes:
                logger.warning("No price/volume data fetched. Retrying.")
                time.sleep(5)
                continue

            # 2a) Filter spurious aggregated data if toggle is on
            filtered_prices, filtered_volumes = filter_spurious_data(prices, volumes)

            # 3) Calculate VWAP, bands
            vwap, upper_band, lower_band, std_dev = calculate_vwap_and_bands(filtered_prices, filtered_volumes)
            if vwap is None:
                log_message_throttled("Not enough data to calculate VWAP. Skipping cycle.", "vwap_error")
                time.sleep(5)
                continue

            current_vwap_data = {
                "vwap": vwap,
                "upper_band": upper_band,
                "lower_band": lower_band
            }
            log_message_throttled(
                f"VWAP: {vwap:.2f}, U: {upper_band:.2f}, L: {lower_band:.2f}, StdDev: {std_dev:.2f}",
                "vwap_info"
            )

            # 4) Fetch current (live) price & filter if toggle is on
            try:
                # Get latest trade request
                request = StockLatestTradeRequest(symbol_or_symbols=SYMBOL)
                latest_trades = client.get_stock_latest_trade(request)

                if SYMBOL in latest_trades:
                    last_trade = latest_trades[SYMBOL]
                    raw_live_price = last_trade.price
                else:
                    logger.warning("Failed to fetch current price. Retrying.")
                    time.sleep(5)
                    continue
            except Exception as e:
                logger.warning(f"Failed to fetch current price: {e}. Retrying.")
                time.sleep(5)
                continue

            filtered_live_price = filter_live_price(raw_live_price)
            if filtered_live_price is None:
                logger.info("Skipping cycle due to spurious live price tick.")
                time.sleep(5)
                continue

            current_price = filtered_live_price
            write_json(CURRENT_PRICE_FILE, {"current_price": current_price})
            log_message_throttled(f"Current Price: {current_price}", "price_info")

            # 5) Close positions if exit conditions are met (includes manual positions)
            close_positions_if_exit_condition_met(current_price, vwap, std_dev)

            # 6) Open new positions if conditions are met (VWAP logic)
            open_new_positions(current_price, vwap, upper_band, lower_band, std_dev)

            # 7) Process manual trades (entry logic and marking)
            process_manual_trades(current_price)

            # 8) Heartbeat
            if (now - last_heartbeat) >= timedelta(minutes=HEARTBEAT_FREQUENCY_MINUTES):
                log_heartbeat()
                last_heartbeat = now

            time.sleep(5)

        except Exception as e:
            logger.exception(f"Unexpected error in the trading loop: {e}")
            time.sleep(5)

# Graceful shutdown signals
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

if __name__ == "__main__":
    run_trading_bot()
