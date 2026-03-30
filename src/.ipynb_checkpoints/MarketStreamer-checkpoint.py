import zmq
import time
import json
import pandas as pd

def stream_data(file_path, port=5555):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)  # Publisher pattern
    socket.bind(f"tcp://*:{port}")

    df = pd.read_csv(file_path)
    print(f"Starting stream on port {port}...")

    for _, row in df.iterrows():
        message = {
            "symbol": row['symbol'],
            "price": row['price'],
            "timestamp": time.time() # For Telemetry
        }
        socket.send_json(message)
        time.sleep(0.1)  # Simulates high-throughput market

if __name__ == "__main__":
    stream_data("data/stocks.csv")