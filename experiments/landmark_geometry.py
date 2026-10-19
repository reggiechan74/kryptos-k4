"""Stdlib WGS84/UTM33 and radial polygon support for a frozen axis audit."""
import math
A=6378137.; F=1/298.257223563; B=A*(1-F); E2=F*(2-F)
ORIGIN=(52.5211638,13.4133059)

def utm(lat,lon):
    p=math.radians(lat);l=math.radians(lon-15);ep=E2/(1-E2);n=A/math.sqrt(1-E2*math.sin(p)**2);t=math.tan(p)**2;c=ep*math.cos(p)**2;aa=math.cos(p)*l
    m=A*((1-E2/4-3*E2**2/64-5*E2**3/256)*p-(3*E2/8+3*E2**2/32+45*E2**3/1024)*math.sin(2*p)+(15*E2**2/256+45*E2**3/1024)*math.sin(4*p)-35*E2**3/3072*math.sin(6*p))
    x=500000+.9996*n*(aa+(1-t+c)*aa**3/6+(5-18*t+t*t+72*c-58*ep)*aa**5/120)
    y=.9996*(m+n*math.tan(p)*(aa*aa/2+(5-t+9*c+4*c*c)*aa**4/24+(61-58*t+t*t+600*c-330*ep)*aa**6/720))
    return x,y

def unutm(x,y):
    e1=(1-math.sqrt(1-E2))/(1+math.sqrt(1-E2));mu=(y/.9996)/(A*(1-E2/4-3*E2**2/64-5*E2**3/256))
    p=mu+(3*e1/2-27*e1**3/32)*math.sin(2*mu)+(21*e1**2/16-55*e1**4/32)*math.sin(4*mu)+151*e1**3/96*math.sin(6*mu)+1097*e1**4/512*math.sin(8*mu)
    ep=E2/(1-E2);n=A/math.sqrt(1-E2*math.sin(p)**2);r=A*(1-E2)/(1-E2*math.sin(p)**2)**1.5;t=math.tan(p)**2;c=ep*math.cos(p)**2;d=(x-500000)/(n*.9996)
    lat=p-n*math.tan(p)/r*(d*d/2-(5+3*t+10*c-4*c*c-9*ep)*d**4/24+(61+90*t+298*c+45*t*t-252*ep-3*c*c)*d**6/720)
    lon=math.radians(15)+(d-(1+2*t+c)*d**3/6+(5-2*c+28*t-3*c*c+8*ep+24*t*t)*d**5/120)/math.cos(p)
    return math.degrees(lat),math.degrees(lon)

def inverse(lat1,lon1,lat2,lon2):
    if abs(lat1-lat2)+abs(lon1-lon2)<1e-14:return 0.,0.
    u1=math.atan((1-F)*math.tan(math.radians(lat1)));u2=math.atan((1-F)*math.tan(math.radians(lat2)));s1,c1=math.sin(u1),math.cos(u1);s2,c2=math.sin(u2),math.cos(u2);L=math.radians(lon2-lon1);lam=L
    for _ in range(100):
        sl,cl=math.sin(lam),math.cos(lam);ss=math.hypot(c2*sl,c1*s2-s1*c2*cl);cs=s1*s2+c1*c2*cl;sigma=math.atan2(ss,cs);sa=c1*c2*sl/ss;ca2=1-sa*sa;cm=cs-2*s1*s2/ca2 if ca2>1e-15 else 0.;C=F/16*ca2*(4+F*(4-3*ca2));old=lam;lam=L+(1-C)*F*sa*(sigma+C*ss*(cm+C*cs*(-1+2*cm*cm)))
        if abs(lam-old)<1e-13:break
    else:raise ValueError('Vincenty inverse didnotconverge')
    u=ca2*(A*A-B*B)/(B*B);aa=1+u/16384*(4096+u*(-768+u*(320-175*u)));bb=u/1024*(256+u*(-128+u*(74-47*u)));delta=bb*ss*(cm+bb/4*(cs*(-1+2*cm*cm)-bb/6*cm*(-3+4*ss*ss)*(-3+4*cm*cm)))
    return B*aa*(sigma-delta),math.degrees(math.atan2(c2*math.sin(lam),c1*s2-s1*c2*math.cos(lam)))%360

def direct(lat,lon,bearing,distance):
    al=math.radians(bearing);u=math.atan((1-F)*math.tan(math.radians(lat)));su,cu=math.sin(u),math.cos(u);sa=cu*math.sin(al);ca2=1-sa*sa;sig1=math.atan2(math.tan(u),math.cos(al));us=ca2*(A*A-B*B)/(B*B);aa=1+us/16384*(4096+us*(-768+us*(320-175*us)));bb=us/1024*(256+us*(-128+us*(74-47*us)));sig=distance/(B*aa)
    for _ in range(100):
        cm=math.cos(2*sig1+sig);ss,cs=math.sin(sig),math.cos(sig);de=bb*ss*(cm+bb/4*(cs*(-1+2*cm*cm)-bb/6*cm*(-3+4*ss*ss)*(-3+4*cm*cm)));old=sig;sig=distance/(B*aa)+de
        if abs(sig-old)<1e-13:break
    else:raise ValueError('Vincenty direct didnotconverge')
    ss,cs=math.sin(sig),math.cos(sig);tmp=su*ss-cu*cs*math.cos(al);p=math.atan2(su*cs+cu*ss*math.cos(al),(1-F)*math.hypot(sa,tmp));lam=math.atan2(ss*math.sin(al),cu*cs-su*ss*math.cos(al));C=F/16*ca2*(4+F*(4-3*ca2));L=lam-(1-C)*F*sa*(sig+C*ss*(math.cos(2*sig1+sig)+C*cs*(-1+2*math.cos(2*sig1+sig)**2)))
    return math.degrees(p),lon+math.degrees(L)

def radial(x,y):
    lat,lon=unutm(x,y);r,b=inverse(*ORIGIN,lat,lon);b=math.radians(b);return r*math.sin(b),r*math.cos(b)

def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def segdist(p,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1];den=dx*dx+dy*dy;t=max(0.,min(1.,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0.
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def in_ring(p,ring):
    inside=False
    for a,b in zip(ring,ring[1:]):
        if segdist(p,a,b)<1e-7:return 0
        if (a[1]>p[1])!=(b[1]>p[1]) and p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]:inside=not inside
    return 1 if inside else -1

def inside(p,polys):
    for rings in polys:
        out=in_ring(p,rings[0])
        if out<0:continue
        if out==0:return True
        holes=[in_ring(p,h) for h in rings[1:]]
        if 0 in holes or not any(v>0 for v in holes):return True
    return False

def bbox(polys):
    pts=[p for rings in polys for ring in rings for p in ring];return min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)
def area(polys):
    def ar(r):
        x,y=r[0];return abs(sum((a[0]-x)*(b[1]-y)-(b[0]-x)*(a[1]-y) for a,b in zip(r,r[1:])))/2
    return sum(ar(rs[0])-sum(ar(r) for r in rs[1:]) for rs in polys)
def segments(polys):return [(a,b) for rs in polys for r in rs for a,b in zip(r,r[1:]) if a!=b]
def contained(child,parent):
    ps=segments(parent)
    for a,b in segments(child):
        if not inside(a,parent) or not inside(((a[0]+b[0])/2,(a[1]+b[1])/2),parent):return False
        for c,d in ps:
            if cross(a,b,c)*cross(a,b,d)<-1e-12 and cross(c,d,a)*cross(c,d,b)<-1e-12:return False
    return True

def merge_intervals(items,period=360):
    out=[]
    for lo,hi in sorted(items):
        if out and lo<=out[-1][1]+1e-10:out[-1][1]=max(out[-1][1],hi)
        else:out.append([lo,hi])
    return out

def segment_support(a,b,R=5000):
    dx,dy=b[0]-a[0],b[1]-a[1];v=dx*dx+dy*dy
    if segdist((0,0),a,b)<1e-9:return [[0.,360.]]
    if not v:
        if math.hypot(*a)>R:return []
        t=math.degrees(math.atan2(a[0],a[1]))%360;return [[t,t]]
    q=a[0]*dx+a[1]*dy;c=a[0]**2+a[1]**2-R*R;disc=q*q-v*c
    if disc<0:return []
    root=math.sqrt(max(0.,disc));lo=max(0.,(-q-root)/v);hi=min(1.,(-q+root)/v)
    if lo>hi:return []
    p=(a[0]+lo*dx,a[1]+lo*dy);q=(a[0]+hi*dx,a[1]+hi*dy);t1=math.degrees(math.atan2(p[0],p[1]))%360;t2=math.degrees(math.atan2(q[0],q[1]))%360;delta=(t2-t1+180)%360-180
    start=(t1 if delta>=0 else t2)%360;end=start+abs(delta)
    return [[start,min(360.,end)]]+([[0.,end-360.]] if end>360 else [])

def support(polys,step):
    if inside(utm(*ORIGIN),polys):return [[0.,360.]],True
    intervals=[]
    for a,b in segments(polys):
        n=max(1,math.ceil(math.dist(a,b)/step));prev=radial(*a)
        for j in range(1,n+1):
            p=radial(a[0]+(b[0]-a[0])*j/n,a[1]+(b[1]-a[1])*j/n);intervals.extend(segment_support(prev,p));prev=p
    return merge_intervals(intervals),False

def axis_intervals(directional):
    out=[]
    for lo,hi in directional:
        length=hi-lo
        if length>=180:return [[0.,180.]]
        start=lo%180;end=start+length;out.append([start,min(180.,end)])
        if end>180:out.append([0.,end-180])
    return merge_intervals(out,180)

def hit(intervals,angle):return any(a-1e-9<=angle<=b+1e-9 for a,b in intervals)
