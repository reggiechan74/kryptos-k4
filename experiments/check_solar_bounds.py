"""Conditional analytic horizon bounds only; no ephemeris/date or key search."""
import json
from math import sin,cos,asin,atan2,hypot,radians,degrees
phi=radians(38.95); cap=radians(23.44)
records=[]
for az in (67.5,247.5):
    a=sin(phi);b=cos(phi)*cos(radians(az));radius=hypot(a,b)
    h=asin(sin(cap)/radius)-atan2(b,a)
    lower=asin(b)
    assert abs((a*sin(h)+b*cos(h))-sin(cap))<1e-12
    records.append({'solar_azimuth_clockwise_true_north_deg':az,'minimum_declination_above_geometric_horizon_deg':degrees(lower),'maximum_geometric_elevation_deg':degrees(h)})
assert round(records[0]['minimum_declination_above_geometric_horizon_deg'],2)==17.31
assert round(records[0]['maximum_geometric_elevation_deg'],2)==9.55
assert round(records[1]['maximum_geometric_elevation_deg'],2)==60.22
print(json.dumps({'check':'SOLAR-BOUNDS-NOTE-001','latitude_deg':38.95,'assumed_annual_declination_cap_deg':23.44,'method':'sin(delta)=sin(phi)sin(h)+cos(phi)cos(h)cos(A); analytic root at declination cap; geometric center and unobstructed horizon, no refraction','conditional_bounds':records,'date_time_search_performed':False,'optical_key_search_performed':False,'reflections_modelled':False,'site_geometry_measured':False},indent=2))
