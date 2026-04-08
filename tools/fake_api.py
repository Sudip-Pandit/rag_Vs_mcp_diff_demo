import random
import time

def simulate_latency(min_ms=50, max_ms=300):
    """Simulates network latency."""
    time.sleep(random.uniform(min_ms/1000, max_ms/1000))

def simulate_failure(probability=0.1):
    """Randomly simulate API failure."""
    if random.random() < probability:
        raise Exception("Simulated API timeout/error")