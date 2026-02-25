import h3

def get_h3_index(lat: float, lng: float, resolution: int = 8) -> str:
    """Возвращает H3 индекс в виде строки (hex)"""
    return h3.latlng_to_cell(lat, lng, resolution)

def get_neighbors(h3_index: str, k: int = 1):
    """Соседние гексы"""
    return [h3.cell_to_string(c) for c in h3.grid_disk(h3_index, k)]