import zmq
from Telemetry import TelemetryTracker

def run_worker(master_ip):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{master_ip}:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    # Initialize Telemetry
    tracker = TelemetryTracker()
    prices = []

    print("Worker started. Tracking latency...")

    while True:
        data = socket.recv_json()
        
        # Perform your logic
        prices.append(data['price'])
        # ... (Moving average logic here) ...
        
        # RECORD THE PERFORMANCE
        latency = tracker.record_metric(data['symbol'], data['sent_at'])
        
        # Required Output Format
        print(f"{{'symbol': '{data['symbol']}', 'price': {data['price']}}}: ACTION (Latency: {latency:.2f}ms)")