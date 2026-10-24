"""Conditional solar and direct-ray constraints; no ciphertext or measured geometry."""
import argparse
import calendar
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import resource
import sys
from pathlib import Path
import time

R = math.radians
D = math.degrees

def clamp(x):
    return max(-1.0, min(1.0, x))

def required_declination(latitude, azimuth, altitude):
    p, a, h = map(R, (latitude, azimuth, altitude))
    return D(math.asin(clamp(math.sin(p)*math.sin(h)+math.cos(p)*math.cos(h)*math.cos(a))))

def horizontal(latitude, declination, hour_angle):
    """Observer-to-body vector, east/north/up; azimuth clockwise true north."""
    p, d, H = map(R, (latitude, declination, hour_angle))
    east = -math.cos(d)*math.sin(H)
    north = math.sin(d)*math.cos(p)-math.cos(d)*math.cos(H)*math.sin(p)
    up = math.sin(d)*math.sin(p)+math.cos(d)*math.cos(H)*math.cos(p)
    return {'azimuth': D(math.atan2(east, north)) % 360,
            'altitude': D(math.atan2(up, math.hypot(east, north))),
            'enu': [east, north, up]}

def envelope(latitude, azimuth, cap, minimum_altitude):
    p, a = R(latitude), R(azimuth)
    x, y = math.sin(p), math.cos(p)*math.cos(a)
    amplitude, phase = math.hypot(x, y), math.atan2(y, x)
    lo, hi = R(minimum_altitude), math.pi/2
    points = [lo, hi]
    # Solve both signed declination boundaries, including all branches.
    for target in (-math.sin(R(cap)), math.sin(R(cap))):
        if abs(target) <= amplitude:
            theta = math.asin(target/amplitude)
            for base in (theta-phase, math.pi-theta-phase):
                for turn in range(-2, 3):
                    h = base+turn*2*math.pi
                    if lo < h < hi:
                        points.append(h)
    points = sorted(set(points))
    intervals = []
    for left, right in zip(points, points[1:]):
        middle = (left+right)/2
        if abs(x*math.sin(middle)+y*math.cos(middle)) <= math.sin(R(cap))+1e-14:
            intervals.append([D(left), D(right)])
    extrema = [lo, hi]
    for turn in range(-2, 3):
        h = math.pi/2-phase+turn*math.pi
        if lo <= h <= hi:
            extrema.append(h)
    ds = [D(math.asin(clamp(x*math.sin(h)+y*math.cos(h)))) for h in extrema]
    return {'latitude': latitude, 'true_azimuth': azimuth, 'declination_cap': cap,
            'minimum_center_altitude': minimum_altitude,
            'reachable_altitude_intervals': intervals,
            'declination_extrema_over_altitude_domain': [min(ds), max(ds)]}

def solar_usno(instant):
    """USNO approximate geocentric solar coordinates; UTC used as UT approximation."""
    if instant.tzinfo is None:
        raise ValueError('timezone required')
    jd = instant.timestamp()/86400+2440587.5
    day = jd-2451545
    g, q = (357.529+.98560028*day) % 360, (280.459+.98564736*day) % 360
    lon = (q+1.915*math.sin(R(g))+.020*math.sin(2*R(g))) % 360
    eps = 23.439-.00000036*day
    ra = D(math.atan2(math.cos(R(eps))*math.sin(R(lon)), math.cos(R(lon)))) % 360
    dec = D(math.asin(math.sin(R(eps))*math.sin(R(lon))))
    eot = ((q-ra+180) % 360-180)*4
    return {'jd': jd, 'declination': dec, 'equation_of_time_minutes': eot,
            'ecliptic_longitude': lon, 'obliquity': eps}

def solar_noaa(instant):
    year_days = 366 if calendar.isleap(instant.year) else 365
    hour = instant.hour+instant.minute/60+instant.second/3600
    gamma = 2*math.pi/year_days*(instant.timetuple().tm_yday-1+(hour-12)/24)
    dec = (.006918-.399912*math.cos(gamma)+.070257*math.sin(gamma)
           -.006758*math.cos(2*gamma)+.000907*math.sin(2*gamma)
           -.002697*math.cos(3*gamma)+.00148*math.sin(3*gamma))
    eqt = 229.18*(.000075+.001868*math.cos(gamma)-.032077*math.sin(gamma)
                   -.014615*math.cos(2*gamma)-.040849*math.sin(2*gamma))
    return {'declination': D(dec), 'equation_of_time_minutes': eqt}

def ray_plane(source, aperture, receiver_height):
    """Forward transmitted ray after aperture; no obstruction or optical-shape claim."""
    direction = [p-s for p, s in zip(aperture, source)]
    if all(v == 0 for v in direction):
        return {'status': 'degenerate_source_at_aperture'}
    if direction[2] == 0:
        return {'status': 'coplanar' if aperture[2] == receiver_height else 'parallel_disjoint'}
    t = (receiver_height-aperture[2])/direction[2]
    return {'status': 'forward' if t >= 0 else 'behind_aperture', 't': t,
            'intersection': [p+t*v for p, v in zip(aperture, direction)]}

def date_samples():
    samples = []
    for date in ('1969-09-30', '1990-11-03', '1990-11-05'):
        start = datetime.fromisoformat(date).replace(tzinfo=timezone.utc)
        for hours in (0, 12, 24):
            samples.append(('source_date_endpoint_or_noon', start+timedelta(hours=hours)))
    for day in range(1, 31):
        samples.append(('month_inventory_noon_not_event_time', datetime(1988, 11, day, 12, tzinfo=timezone.utc)))
    return samples

def independent_grid_check(record, steps=10000):
    # Direct vector dot product in a separately constructed orthonormal frame;
    # grid membership is checked only, not used to find analytical roots.
    p, a = R(record['latitude']), R(record['true_azimuth'])
    pole = (0.0, math.cos(p), math.sin(p))
    for j in range(steps+1):
        h = record['minimum_center_altitude']+(90-record['minimum_center_altitude'])*j/steps
        v = (math.cos(R(h))*math.sin(a), math.cos(R(h))*math.cos(a), math.sin(R(h)))
        delta = D(math.asin(clamp(sum(u*w for u, w in zip(pole, v)))))
        direct = abs(delta) <= record['declination_cap']+1e-10
        intervals = any(left-1e-10 <= h <= right+1e-10 for left, right in record['reachable_altitude_intervals'])
        if direct != intervals:
            raise AssertionError(('grid/root disagreement', record, h, delta))
    return steps+1

def run_checks():
    start = time.monotonic()
    records = [envelope(p, a, cap, h) for p in (38.94, 38.951, 38.96)
               for a in (56.25, 67.5, 78.75, 236.25, 247.5, 258.75, 57.872, 237.872)
               for cap in (23.44, 23.5) for h in (0, -.833)]
    grid_checks = sum(independent_grid_check(row) for row in records)
    dates = []
    for role, instant in date_samples():
        usno, noaa = solar_usno(instant), solar_noaa(instant)
        dd = abs(usno['declination']-noaa['declination'])
        de = abs(usno['equation_of_time_minutes']-noaa['equation_of_time_minutes'])
        if dd > .75 or de > 2:
            raise AssertionError(('predeclared approximation tolerance', instant, dd, de))
        dates.append({'role': role, 'utc': instant.isoformat(), 'usno': usno, 'noaa': noaa,
                      'declination_difference': dd, 'eot_difference_minutes': de})
    rays = []
    for source_height in range(-2, 3):
        for aperture_height in range(-2, 3):
            for receiver_height in range(-2, 3):
                result = ray_plane([0, 0, source_height], [1, 2, aperture_height], receiver_height)
                if source_height < receiver_height < aperture_height:
                    assert result['status'] == 'behind_aperture'
                if 'intersection' in result:
                    assert abs(result['intersection'][2]-receiver_height) < 1e-12
                rays.append({'source_z': source_height, 'aperture_z': aperture_height,
                             'receiver_z': receiver_height, 'result': result})
    legacy = [envelope(38.95, a, 23.44, 0) for a in (67.5, 247.5)]
    elapsed = time.monotonic()-start
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes = rss if sys.platform == 'darwin' else rss*1024
    if rss_bytes > 256*1024*1024:
        raise MemoryError('frozen 256-MiB quantitative budget')
    if elapsed > 60:
        raise TimeoutError('frozen 60-second quantitative budget')
    return {'scope': 'conditional physical constraints; no K4 evaluation or measured installed geometry',
            'prior_coverage_reproduced': legacy, 'envelopes': records,
            'old_model_pair_conditional_required_declination': required_declination(38.951, 72, 40),
            'dates': dates, 'ray_cases': rays,
            'controls': {'independent_grid_checks': grid_checks, 'date_cross_checks': len(dates),
                         'ray_substitution_cases': len(rays), 'all_passed': True},
            'elapsed_seconds': elapsed, 'peak_rss_bytes': rss_bytes}

def main():
    from run_io import RunSnapshot, json_bytes, specification
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec-commit', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--kind', choices=('original', 'replay'), default='replay')
    args = parser.parse_args()
    spec_path = Path('research/PHYSICAL-SOLAR-002-SPEC.md')
    spec = specification(args.spec_commit, spec_path)
    with RunSnapshot(args.output, 'PHYSICAL-SOLAR-002', spec, execution_kind=args.kind) as snapshot:
        result = run_checks()
        result['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        snapshot.write('physical-checks.json', json_bytes(result))
    print(snapshot.final)

if __name__ == '__main__':
    main()
