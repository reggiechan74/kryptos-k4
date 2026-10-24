#!/usr/bin/env python3
"""Read-only integrity/structure check. This does not clear source rights or survey accuracy."""
import ast
import csv
import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path, PurePosixPath
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_MAPS = [
    'Berlin-WSW-around-the-world.png',
    'Berlin-WSW-country-polygon-intersections.png',
    'Kremlin-sphere-vs-WGS84.png',
    'Berlin-WSW-Mapped-footprint-crossings-and-misses.png',
]
TABLE_ROWS = {
    'Berlin-WSW-Nearby-points-not-intersections.csv': 104,
    'Berlin-WSW-Modeled-country-polygon-intersections.csv': 45,
    'Berlin-WSW-Integrated-modeled-intersections-and-tested-misses.csv': 147,
}

def safe_relative(name):
    p = PurePosixPath(name)
    return not p.is_absolute() and bool(p.parts) and not any(x in ('..', '.') for x in p.parts) and '\\' not in name

def png_info(path):
    b = path.read_bytes()
    assert b[:8] == b'\x89PNG\r\n\x1a\n', path
    offset = 8
    dimensions = None
    ended = False
    while offset < len(b):
        length = struct.unpack('>I', b[offset:offset+4])[0]
        kind = b[offset+4:offset+8]
        payload = b[offset+8:offset+8+length]
        crc = struct.unpack('>I', b[offset+8+length:offset+12+length])[0]
        assert zlib.crc32(kind+payload) & 0xffffffff == crc, (path, kind)
        if kind == b'IHDR': dimensions = struct.unpack('>II', payload[:8])
        offset += length+12
        if kind == b'IEND': ended = True; break
    assert ended and offset == len(b) and dimensions and min(dimensions) > 0, path
    return dimensions

def main():
    manifest = json.loads((ROOT/'manifest.json').read_text())
    expected = {r['path']: r for r in manifest['files']}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    assert actual == set(expected), {'missing': sorted(set(expected)-actual), 'extra': sorted(actual-set(expected))}
    for name, entry in expected.items():
        assert safe_relative(name), name
        p = ROOT/name
        assert not p.is_symlink(), name
        b = p.read_bytes()
        assert len(b) == entry['bytes'] and hashlib.sha256(b).hexdigest() == entry['sha256'], name
        if p.suffix == '.py': ast.parse(b, filename=name)
        elif p.suffix == '.svg': ET.fromstring(b)
        elif p.suffix in ('.json', '.geojson'): json.loads(b)
    dimensions = {n: png_info(ROOT/'maps'/n) for n in REQUIRED_MAPS}
    counts = {}
    for name, count in TABLE_ROWS.items():
        with (ROOT/'tables'/name).open(newline='') as f: rows=list(csv.DictReader(f))
        assert len(rows) == count, (name,len(rows),count)
        counts[name] = len(rows)
        if 'Integrated' in name: assert sum(r['relationship'] == 'misses tested footprint' for r in rows) == 34
        if 'Modeled-country' in name: assert len({r['country'] for r in rows}) == 17
    for name in ['derived/route.geojson', 'derived/country_polygon_intersections.geojson']:
        d=json.loads((ROOT/name).read_text());assert d['type']=='FeatureCollection' and d['features']
    report = {'passed': True, 'payload_files': len(expected), 'required_maps': dimensions, 'table_rows': counts,
              'scope':'Archive integrity, syntax, PNG chunks and stated row counts only; not a full data rebuild or rights clearance.'}
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
