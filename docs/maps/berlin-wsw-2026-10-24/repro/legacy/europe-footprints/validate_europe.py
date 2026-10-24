import verify_footprints as v
from verify_footprints import *
from shapely import get_coordinates
# Verify the independently constructed route against the parent's published line.
parent=json.loads((P.parent/'route.geojson').read_text());coords=get_coordinates(shape(parent['features'][0]['geometry']));px,py=project(coords[:,0],coords[:,1]);plane_error=float(np.max(np.abs(py))*1000)
# Classic forward great-circle formula (separate from vector construction).
maxerr=0
for s in np.linspace(0,C,101):
 la=math.radians(52.521146530576253);lo=math.radians(13.4133090391431029);az=math.radians(247.5);a=s/R
 phi=math.asin(math.sin(la)*math.cos(a)+math.cos(la)*math.sin(a)*math.cos(az));lam=lo+math.atan2(math.sin(az)*math.sin(a)*math.cos(la),math.cos(a)-math.sin(la)*math.sin(phi));ll=unproject(float(s));delta=abs((math.degrees(lam)-ll[0]+180)%360-180);maxerr=max(maxerr,delta,abs(math.degrees(phi)-ll[1]))
row=json.loads((P/'moscow_kremlin_nominatim.json').read_text())[0]
coarse,_=analyze(row,'Kremlin');old=v.segmentize;v.segmentize=lambda g,s:old(g,.000005);fine,_=v.analyze(row,'Kremlin');v.segmentize=old
err=max(abs(coarse['intervals'][0][k]-fine['intervals'][0][k])*1000 for k in ['entry_km','exit_km'])
# Compare with original parent 0.5km-sampled lon/lat route intersection.
parcut=shape(parent['features'][0]['geometry']).intersection(shape(row['geojson']));ends=sorted(project(*c)[0] for c in list(parcut.coords)[::len(parcut.coords)-1]);diff=max(abs(ends[0]-fine['intervals'][0]['entry_km']),abs(ends[1]-fine['intervals'][0]['exit_km']))*1000
out={'max_parent_route_spherical_plane_residual_m':plane_error,'max_independent_classic_formula_difference_degrees':maxerr,'Kremlin_entry_exit_change_after_10x_boundary_refinement_m':err,'Kremlin_entry_exit_parent_sampled_route_vs_refined_sphere_max_difference_m':diff,'interpretation':'Numerical agreement does not establish input coordinate, initial bearing, boundary, or spherical Earth model accuracy.'}
(P/'numerical_validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
