import pandas as pd
import os
from logger import get_logger

logger = get_logger(__name__)

def extract():
    try:
        logger.info("Data extract start...")
        df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "superstore_sales.csv"), encoding="latin-1")
        logger.info("Data extract concluded")
        return df
    except Exception as e:
        logger.error(f"Ocurred some error {e}")
        raise