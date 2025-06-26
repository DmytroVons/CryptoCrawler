FETCH_INTERVAL = 1  # seconds
API_URL = "https://api.coingecko.com/api/v3/simple/price"
QUERY_PARAMS = {
    "ids": "bitcoin",
    "vs_currencies": "usd",
    "include_last_updated_at": "true"
}
SMA_WINDOW_SIZE = 10
MAX_RETRIES = 5
