"""Shared metre-space strap route and distance-based texture coordinates."""
import math
KNOTS=[(-.050,-.001,.136),(-.058,-.003,.108),(-.069,-.006,.063),(-.075,-.012,.030),(-.070,-.037,.008),(-.052,-.058,.003),(-.023,-.065,.003),(0,-.066,.003),(.023,-.065,.003),(.052,-.058,.003),(.070,-.037,.008),(.075,-.012,.030),(.069,-.006,.063),(.058,-.003,.108),(.050,-.001,.136)]
def sample_route():
 points=[]
 for i in range(len(KNOTS)-1):
  p0,p1,p2,p3=[KNOTS[j] for j in (max(0,i-1),i,i+1,min(len(KNOTS)-1,i+2))]
  for j in range(18):
   t=j/18;points.append(tuple(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t) for a,b,c,d in zip(p0,p1,p2,p3)))
 points.append(KNOTS[-1]);distance=[0.]
 for a,b in zip(points,points[1:]):distance.append(distance[-1]+math.dist(a,b))
 return points,distance
POINTS,DISTANCES=sample_route();LENGTH=DISTANCES[-1];TEXTURE_HEIGHT=round(LENGTH/.014*256)
def motif_positions():
 # Same physical height as the approved earlier photographs (y945 / 1536).
 eye=(0,-.433503,.163);norm=math.sqrt(sum(v*v for v in eye));z=tuple(v/norm for v in eye)
 norm=math.hypot(z[0],z[1]);right=(-z[1]/norm,z[0]/norm,0)
 up=(z[1]*right[2]-z[2]*right[1],z[2]*right[0]-z[0]*right[2],z[0]*right[1]-z[1]*right[0])
 def py(p):return (.5-sum((v-t)*u for v,t,u in zip(p,(0,0,.127),up))/.30)*1536
 indices=[min([i for i,p in enumerate(POINTS) if p[0]*side>0 and p[2]>.025],key=lambda i:abs(py(POINTS[i])-945)) for side in (-1,1)]
 return [(1-DISTANCES[i]/LENGTH)*TEXTURE_HEIGHT for i in indices]
