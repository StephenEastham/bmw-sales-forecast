"""
Utility functions: logging, paths, and helpers
"""

import logging
from config import out_path


def setup_logger(log_file='sales_alerts.log'):
    """Setup logging to file and console"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(out_path(log_file)),
            logging.StreamHandler()
        ],
        force=True
    )
    return logging.getLogger(__name__)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(title)
    print("="*80)
