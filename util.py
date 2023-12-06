from haversine import haversine

def cal_dis(s_Lng, s_Lat, w_Lng, w_Lat) -> float:
    d1 = (s_Lat, s_Lng)
    d2 = (w_Lat, w_Lng)
    dis = haversine(d1, d2) * 1000
    result = "%.7f" % dis
    return float(result)
