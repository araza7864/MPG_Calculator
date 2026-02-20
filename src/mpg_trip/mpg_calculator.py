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
    return 1 / ((1 - highway_weight) / city_mpg + highway_weight / highway_mpg)