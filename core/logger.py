from logging import basicConfig, INFO, getLogger

basicConfig(
    level=INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

log = getLogger("CryptoCrawler")
