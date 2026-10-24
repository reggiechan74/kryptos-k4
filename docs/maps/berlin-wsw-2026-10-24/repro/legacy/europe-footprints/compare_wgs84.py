import sys;
from geographiclib.geodesic import Geodesic
from scipy.optimize import minimize_scalar
from verify_footprints import *
from shapely import get_coordinates
G=Geodesic.WGS84;line=G.Line(52.521146530576253,13.4133090391431029,247.5)
# Independent ellipsoid calculation only. The mapped spherical route is NOT changed.
geom=shape(json.loads((P/'moscow_kremlin_nominatim.json').read_text())[0]['geojson'])
verts=get_coordinates(segmentize(geom,0.0001))
center=(55.7516212,37.6181220)
def pos(s):return line.Position(s)
def distance_to_point(s,lat,lon):
 q=pos(s);return G.Inverse(q['lat2'],q['lon2'],lat,lon)['s12']
center_min=minimize_scalar(lambda s:distance_to_point(s,*center),bounds=(38000000,39000000),method='bounded',options={'xatol':.0001})
best=None
for lon,lat in verts:
 opt=minimize_scalar(lambda s:distance_to_point(s,float(lat),float(lon)),bounds=(center_min.x-10000,center_min.x+10000),method='bounded',options={'xatol':.001})
 if best is None or opt.fun<best[0]:best=(float(opt.fun),float(opt.x),float(lon),float(lat))
endpoint=pos(C*1000);gap=G.Inverse(endpoint['lat2'],endpoint['lon2'],52.521146530576253,13.4133090391431029)['s12'];near=pos(best[1])
out={'ellipsoid':'WGS84','library':'GeographicLib Python 2.1','initial_bearing_true_degrees':247.5,'spherical_route_unchanged':True,'investigated_wgs84_distance_interval_m':[38000000,39000000],'closest_approach_to_Kremlin_reference_point_m':float(center_min.fun),'closest_approach_to_mapped_Kremlin_polygon_approx_m':best[0],'wgs84_along_distance_at_nearest_m':best[1],'closest_wgs84_route_lonlat':[near['lon2'],near['lat2']],'closest_mapped_boundary_lonlat':[best[2],best[3]],'boundary_sampling_max_degrees':.0001,'interpretation':'Miss. Approximate polygon-distance minimization over boundary vertices densified <=11.12m; not a physically surveyed boundary. Near-return passage after westward launch only, not initial reverse67.5-degree branch.','endpoint_after_sphere_circumference_km':C,'endpoint_lonlat':[endpoint['lon2'],endpoint['lat2']],'endpoint_distance_from_Berlin_origin_m':gap,'documentation_url':'https://geographiclib.sourceforge.io/html/python/code.html'}
(P/'wgs84_comparison.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
