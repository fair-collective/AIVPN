# aivpn/bid/bidder.py
from typing import List, Dict
import json

# Flat ethical rate: $0.01 per recommendation
BID_RATE = 0.01

bids = {}  # title: {company: bid_amount}

def add_bid(title: str, company: str, amount: float):
    if title not in bids:
        bids[title] = {}
    bids[title][company] = amount
    print(f"[BID] {company} bids ${amount} for {title}")

def get_recommendations(title: str, free_options: List[Dict]) -> List[Dict]:
    recs = []
    
    # 1. FREE FIRST
    for opt in free_options:
        recs.append({
            "type": "free",
            "country": opt["country"],
            "service": opt["service"],
            "cost": 0.0,
            "message": f"Free in {opt['country']} on {opt['service']}"
        })
    
    # 2. PAID SECOND
    if title in bids:
        for company, amount in bids[title].items():
            recs.append({
                "type": "paid",
                "company": company,
                "cost": amount,
                "message": f"{company} — ${amount} (ethical bid)"
            })
    
    return recs

# Example
if __name__ == "__main__":
    add_bid("The Office", "Netflix", 0.01)
    free = [{"country": "UK", "service": "BBC iPlayer"}]
    print(json.dumps(get_recommendations("The Office", free), indent=2))
