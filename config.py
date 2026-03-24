import os

# Free trial key — public, rate limited to 10/day
FREE_TRIAL_KEY = "yt_free_trial"
FREE_TIER_LIMIT = 10

# Your paid customer keys go here
# We'll add real ones after deployment
VALID_API_KEYS = set([
    os.getenv("API_KEY_1", ""),
    os.getenv("API_KEY_2", ""),
    os.getenv("API_KEY_3", ""),
])

# Remove empty strings
VALID_API_KEYS.discard("")