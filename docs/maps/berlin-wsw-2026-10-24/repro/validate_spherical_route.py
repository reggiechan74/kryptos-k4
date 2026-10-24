#!/usr/bin/env python3
"""Read-only standard-library checks of the stated spherical route, not real-world accuracy."""
import argparse
import json
import math
from pathlib import Path

LAT = 52.521146530576253
LON = 13.413309039143103
AZ = 247.5
R = 6371.0088
C = 2 * math.pi * R
lat, lon, az = map(math.radians, (LAT, LON, AZ))
u = (math.cos(lat)*math.cos(lon), math.cos(lat)*math.sin(lon), math.sin(lat))
east = (-math.sin(lon), math.cos(lon), 0)
north = (-math.sin(lat)*math.cos(lon), -math.sin(lat)*math.sin(lon), math.cos(lat))
v = tuple(north[i]*math.cos(az)+east[i]*math.sin(az) for i in range(3))
n = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])

def vector_coord(t):
    x, y, z = (math.cos(t)*u[i]+math.sin(t)*v[i] for i in range(3))
    return math.degrees(math.atan2(y, x)), math.degrees(math.atan2(z, math.hypot(x, y)))

def forward_coord(t):
    la = math.asin(math.sin(lat)*math.cos(t)+math.cos(lat)*math.sin(t)*math.cos(az))
    lo = lon+math.atan2(math.sin(az)*math.sin(t)*math.cos(lat), math.cos(t)-math.sin(lat)*math.sin(la))
    return (math.degrees(lo)+180)%360-180, math.degrees(la)

def coordinate_error(a, b):
    return max(abs((a[0]-b[0]+180)%360-180), abs(a[1]-b[1]))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--route', type=Path, default=Path(__file__).resolve().parents[1]/'derived'/'route.geojson', help='Saved route.geojson to validate; defaults to bundled route and is never modified')
    args = parser.parse_args()
    error = max(coordinate_error(vector_coord(i*2*math.pi/16), forward_coord(i*2*math.pi/16)) for i in range(17))
    closure = coordinate_error(vector_coord(0), vector_coord(2*math.pi))
    lo0, la0 = map(math.radians, vector_coord(0))
    lo1, la1 = map(math.radians, vector_coord(1e-7))
    dl = lo1-lo0
    bearing = math.degrees(math.atan2(math.sin(dl)*math.cos(la1), math.cos(la0)*math.sin(la1)-math.sin(la0)*math.cos(la1)*math.cos(dl)))%360
    assert error < 1e-9, error
    assert closure < 1e-9, closure
    assert abs(bearing-AZ) < 1e-5, bearing
    report = {'passed': True, 'model': 'closed spherical great circle, not WGS84', 'radius_km': R,
              'circumference_km': C, 'forward_formula_max_coordinate_error_deg': error,
              'closure_coordinate_error_deg': closure, 'initial_numeric_bearing_deg': bearing,
              'scope': 'Numerical checks only; no boundary, source-coordinate or physical-touch accuracy established.'}
    if args.route:
        data = json.loads(args.route.read_text())
        feature = data['features'][0]
        assert feature['geometry']['type'] == 'MultiLineString'
        parts = feature['geometry']['coordinates']
        coords = [p for part in parts for p in part]
        cross_track = []
        for lo, la in coords:
            lo, la = map(math.radians, (lo, la))
            q = (math.cos(la)*math.cos(lo), math.cos(la)*math.sin(lo), math.sin(la))
            dot = sum(q[i]*n[i] for i in range(3))
            cross_track.append(abs(math.asin(max(-1, min(1, dot)))*R))
        assert coordinate_error(coords[0], (LON, LAT)) < 1e-9
        assert coordinate_error(coords[-1], (LON, LAT)) < 1e-9
        assert max(cross_track) < 1e-6, max(cross_track)
        assert all(abs(b[0]-a[0]) <= 180 for part in parts for a,b in zip(part,part[1:]))
        report['saved_route'] = {'vertices': len(coords), 'antimeridian_split_parts': len(parts),
                                 'max_vertex_cross_track_error_km': max(cross_track)}
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
