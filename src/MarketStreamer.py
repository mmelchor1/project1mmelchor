import zmq
import time
import json
import pandas as pd

def run_market_streamer(file_path="data/stocks.csv"):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555") # Broadcast on port 5555

    df = pd.read_csv(file_path)
    
    for _, row in df.iterrows():
        payload = {
            "symbol": row['symbol'],
            "price": float(row['price']),
            "sent_at": time.time() # Critical for Telemetry 
        }
        socket.send_json(payload)
        time.sleep(0.05) # High-throughput simulation