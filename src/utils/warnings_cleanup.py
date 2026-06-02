import warnings

warnings.filterwarnings(
    "ignore",
    category=FutureWarning
)

warnings.filterwarnings(
    "ignore",
    message=".*LibreSSL.*"
)

warnings.filterwarnings(
    "ignore",
    message=".*Python version 3.9.*"
)
