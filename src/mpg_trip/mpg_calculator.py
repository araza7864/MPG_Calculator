def highway_weight(avg_speed):
    if avg_speed < 25:
        return 0.15
    elif avg_speed < 40:
        return 0.40
    elif avg_speed < 55:
        return 0.70
    else:
        return 0.85


def estimated_mpg(highway_weight, city_mpg, highway_mpg):
    if not 0 <= highway_weight <= 1 or city_mpg <= 0 or highway_mpg <= 0:
        raise ValueError("MPG values must be positive and highway weight must be between 0 and 1.")
    return 1 / ((1 - highway_weight) / city_mpg + highway_weight / highway_mpg)
