#!/usr/bin/env python3
"""Conditional optics arithmetic. No ciphertext, date, coordinates or fitted site geometry."""
import json, math
from pathlib import Path
r=math.radians
phi,A,delta_max=map(r,(38.95,67.5,23.44))
p=math.sin(phi); q=math.cos(phi)*math.cos(A)
hmax=math.asin(math.sin(delta_max)/math.hypot(p,q))-math.atan2(q,p)
d=r(1919/3600); radius=d/2
rows=[]
for hdeg in (math.degrees(hmax),15,30,45,60):
 h=r(hdeg)
 major=d/math.sin(h)**2; minor=d/math.sin(h)
 exact_major=1/math.tan(h-radius)-1/math.tan(h+radius)
 exact_minor=2*math.sin(radius)/math.sqrt(math.sin(h)**2-math.sin(radius)**2)
 rows.append(dict(elevation_deg=hdeg,height_m=1,ground_solar_blur_major_m=major,ground_solar_blur_minor_m=minor,exact_major_m=exact_major,exact_minor_m=exact_minor,heading_error_1deg_first_order_m=1/math.tan(h)*r(1),altitude_error_1deg_first_order_m=r(1)/math.sin(h)**2))
 assert abs(major/exact_major-1)<0.001
 assert abs(minor/exact_minor-1)<0.001
channels=[dict(width_mm=w,thickness_mm=t,zero_overlap_threshold_deg=math.degrees(math.atan(w/t))) for t in (6.35,9.525,12.7) for w in (3,5,10)]
# Positive ray z component cannot hit a lower receiver after the aperture.
for Lz in (-1,0,1):
 for dz in (.001,.1,1,3):
  Az=Lz+dz
  for t in (1.001,2,100): assert Lz+t*(Az-Lz)>Az
out={"status":"conditional_analytical_constraints_not_site_measurements","constants":{"sun_full_angular_diameter_arcsec":1919,"sun_diameter_source":"https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html","illustrative_latitude_deg":38.95,"hypothetical_true_solar_azimuth_deg":67.5,"annual_declination_bound_deg":23.44},"ene_horizon":{"max_geometric_sun_center_elevation_deg":math.degrees(hmax),"obstacle_height_above_aperture_over_distance_cutoff":math.tan(hmax),"declination_needed_at_10deg_elevation":math.degrees(math.asin(p*math.sin(r(10))+q*math.cos(r(10))))},"solar_blur_per_metre_height":rows,"hypothetical_straight_channel_clipping":channels,"checks":{"first_order_blur_matches_exact_conical_footprint_to_0_1_percent":True,"upward_ray_invariant":True},"not_performed":["site survey","aperture contour fit","timestamp inference","cipher or plaintext evaluation","new date/angle search"]}
Path(__file__).with_name('physical-constraints.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
