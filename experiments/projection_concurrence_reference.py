"""Independent scalar determinant and finite-coordinate least-squares checks."""
import math

def intersection(pair1,pair2):
 def coefficients(p):
  (x,y),(u,v)=p['aperture'],p['receiver'];return y-v,u-x,x*v-y*u
 a,b,c=coefficients(pair1);d,e,f=coefficients(pair2)
 return [b*f-c*e,c*d-a*f,a*e-b*d]

def finite_least_squares(pairs):
 aa=ab=bb=ac=bc=0.
 for p in pairs:
  (x,y),(u,v)=p['aperture'],p['receiver'];a,b,c=y-v,u-x,x*v-y*u;n=math.hypot(a,b);a/=n;b/=n;c/=n
  aa+=a*a;ab+=a*b;bb+=b*b;ac+=a*c;bc+=b*c
 det=aa*bb-ab*ab
 if abs(det)<1e-12:raise ValueError('nonunique finite intersection')
 return [(ab*bc-bb*ac)/det,(ab*ac-aa*bc)/det]

def raw_incidence(coords,source):
 x,y,u,v=coords;s,t,w=source
 return (y-v)*s+(u-x)*t+(x*v-y*u)*w

def numerical_gradient(coords,source,step=1e-5):
 out=[]
 for i in range(4):
  a=coords[:];b=coords[:];a[i]+=step;b[i]-=step;out.append((raw_incidence(a,source)-raw_incidence(b,source))/(2*step))
 return out
