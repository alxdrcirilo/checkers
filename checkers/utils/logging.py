import logging

logging.basicConfig(
    level=logging.CRITICAL,
    format="%(asctime)s - %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("checkers.log", mode="w")],
)
