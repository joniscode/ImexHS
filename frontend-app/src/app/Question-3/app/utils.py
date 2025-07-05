import numpy as np
from typing import List

def parse_data(data: List[str]) -> List[float]:
    numbers = []
    for row in data:
        for item in row.split():
            if not item.isdigit():
                raise ValueError("Invalid data entry")
            numbers.append(float(item))
    return numbers

def normalize_data(numbers: List[float]) -> List[float]:
    max_val = max(numbers)
    return [x / max_val for x in numbers] if max_val != 0 else numbers