"""Independent closest-approach cylinder and horizontal-angle reflection oracle."""
import math

def trace(eye,d):
 length=math.sqrt(sum(t*t for t in d));d=tuple(t/length for t in d);horizontal=math.hypot(d[0],d[1]);candidates=[]
 if horizontal>1e-5:
  ux,uy=d[0]/horizontal,d[1]/horizontal;along=-(eye[0]*ux+eye[1]*uy);perp=eye[0]*uy-eye[1]*ux
  if abs(perp)<=1:
   half=math.sqrt(max(0,1-perp*perp))
   for travel in (along-half,along+half):
    distance=travel/horizontal;z=eye[2]+distance*d[2]
    if distance>1e-10 and -1e-9<=z<=2+1e-9:candidates.append((distance,'side'))
 if abs(d[2])>1e-10:
  for z in (0,2):
   distance=(z-eye[2])/d[2];x,y=eye[0]+distance*d[0],eye[1]+distance*d[1]
   if distance>1e-10 and x*x+y*y<=1+1e-9:candidates.append((distance,'cap'))
 if not candidates:return dict(status='miss')
 distance,kind=min(candidates);point=tuple(eye[i]+distance*d[i] for i in range(3))
 if min(abs(point[2]),abs(point[2]-2))<=1e-9 and abs(point[0]**2+point[1]**2-1)<=1e-9:return dict(status='rim')
 if kind=='cap':return dict(status='cap')
 angle=math.atan2(point[1],point[0]);incident=math.atan2(d[1],d[0]);rangle=2*angle-incident+math.pi;r=(horizontal*math.cos(rangle),horizontal*math.sin(rangle),d[2])
 radial=d[0]*math.cos(angle)+d[1]*math.sin(angle)
 if abs(radial)<1e-4:return dict(status='grazing')
 if r[2]>=-1e-8:return dict(status='ground_miss')
 distance2=-point[2]/r[2]
 if distance2<=1e-10:return dict(status='ground_behind')
 ground=tuple(point[i]+distance2*r[i] for i in range(3))
 if ground[0]**2+ground[1]**2<=1+1e-9:return dict(status='inside_cylinder')
 return dict(status='ground',point=ground,hit=point,reflected=r)
