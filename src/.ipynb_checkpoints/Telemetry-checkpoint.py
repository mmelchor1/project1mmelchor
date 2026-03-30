import time
import json

class TelemetryTracker:
    def __init__(self):
        self.log_file = "performance_metrics.csv"
        # Initialize the log file with headers
        with open(self.log_file, "w") as f:
            f.write("symbol,sent_timestamp,action_timestamp,latency_ms\n")

    def record_metric(self, symbol, sent_at):
        """
        Calculates 'tick to action' latency.
        sent_at: The timestamp from the MarketStreamer payload.
        """
        action_at = time.time()
        latency = (action_at - sent_at) * 1000  # Convert to milliseconds
        
        # Save to a local CSV for later analysis/plotting
        with open(self.log_file, "a") as f:
            f.write(f"{symbol},{sent_at},{action_at},{latency:.4f}\n")
        
        return latency