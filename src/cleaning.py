def parse_cell(value):
    """Converts a single CSV string cell into its proper Python type:

    - Empty string -> None (SQL NULL)
    - Whole numbers -> int
    - Decimal numbers -> float
    - Text -> str (unmodified)
    """
    cleaned = value.strip()

    if cleaned == "":
        return None

    try:
        return int(cleaned)
    except ValueError:
        pass

    try:
        return float(cleaned)
    except ValueError:
        pass

    return cleaned


def clean_row_generator(reader):
    """Yields rows where empty strings '' are converted to None (SQL NULL). Numbers are parsed to int and float"""
    for row in reader:
        yield [parse_cell(cell) for cell in row]