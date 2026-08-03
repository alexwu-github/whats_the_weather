def calculate_feels_like(temp_c: float, wind_speed_ms: float) -> float:
    if temp_c > 10 or wind_speed_ms < 1.3:
        return temp_c
    wind_kmh = wind_speed_ms * 3.6
    feels_like = 13.12 + 0.6215 * temp_c - 11.37 * (wind_kmh ** 0.16) + 0.3965 * temp_c * (wind_kmh ** 0.16)
    return round(feels_like, 1)