import csv
import random
from pathlib import Path

random.seed(42)

output = Path("data/synthetic_sellers.csv")
output.parent.mkdir(parents=True, exist_ok=True)

fields = [
    "account_age_days",
    "followers",
    "following",
    "posts",
    "engagement_ratio",
    "has_contact_info",
    "match_count",
    "unique_domains",
    "listed_price",
    "market_median",
    "label",
    "synthetic",
]

with output.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for _ in range(200):
        age = random.randint(1, 2000)
        followers = random.randint(10, 50000)
        following = random.randint(10, 5000)
        posts = random.randint(1, 1000)
        engagement = round(random.uniform(0.001, 0.15), 4)
        contact = random.choice([0, 1])
        matches = random.randint(0, 25)
        domains = random.randint(0, min(matches, 15))
        market = round(random.uniform(100, 20000), 2)
        listed = round(market * random.uniform(0.15, 1.5), 2)

        # Synthetic labels generated from illustrative rules.
        # These are NOT verified real-world fraud labels.
        indicators = (
            (listed < 0.4 * market)
            + (matches >= 10)
            + (age < 30)
            + (followers > 1000 and engagement < 0.01)
            + (contact == 0)
        )

        label = int(indicators >= 2)

        writer.writerow({
            "account_age_days": age,
            "followers": followers,
            "following": following,
            "posts": posts,
            "engagement_ratio": engagement,
            "has_contact_info": contact,
            "match_count": matches,
            "unique_domains": domains,
            "listed_price": listed,
            "market_median": market,
            "label": label,
            "synthetic": True,
        })

print(f"Created {output} with 200 synthetic records.")
