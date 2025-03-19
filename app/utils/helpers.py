import os
import pandas as pd
from typing import List

def get_companies_from_csv(file_path: str) -> List[str]:
    """
    Read CSV file and return list of company names.
    
    Args:
        file_path: Path to CSV file containing company data
        
    Returns:
        List of company names from the CSV
    """
    try:
        if not os.path.exists(file_path):
            return []
        df = pd.read_csv(file_path)
        return df['Company'].unique().tolist()
    
    except Exception:
        return []
