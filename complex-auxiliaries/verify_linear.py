#!/usr/bin/env python3
"""Separate exact/Arb verifier for continuous piecewise-linear density certificates (real or complex roots).
No search-code imports. E1/E3/E6: exact rational arithmetic; E2: FLINT factorization,
certified complex roots, with real roots identified by exact zero imaginary part. E4: analytic antiderivative.
E5: each positive-density cell is tiled by rational bisections. Far edge/root terms
use an Arb Taylor polynomial with a rigorous geometric remainder; near edges use
convex tangents/concave chords or a second derivative lower bound. Near roots use
convex Taylor bounds, or endpoint distance bounds across a root. A quadratic
minorant proves each whole interval. This is same-author independent code, not
independent human or agent review. Credits for certificate criterion: Smith/SO24;
far-field Taylor idea also used by Koshta's checker (read as prior art).
"""
import argparse,json,time,math,hashlib
from fractions import Fraction as Q
from flint import arb,acb,fmpq,fmpz_poly,ctx
if not __debug__:raise SystemExit('refusing python -O')
ctx.prec=160
ORDER=18

def rat(x):
    if type(x) is int:return Q(x)
    if type(x) is str:return Q(x)
    raise ValueError('exact rationals required')
def ball(q):return arb(fmpq(q.numerator,q.denominator))
def G(x):
    if x.is_zero():return arb(0)
    assert not x.contains(0)
    return x*x*(abs(x).log()/2-arb(3)/4)
def enclosed_G(x):
    if not x.contains(0):return G(x)
    v=abs(x).upper()
    if v.is_zero():return arb(0)
    assert v<arb('0.1')
    return arb(0,(v*v*(arb(3)/4-v.log()/2)).upper())
def root_primitive(u):
    # Along a horizontal line off the real axis, Re[z^2(Log z/2-3/4)] is an antiderivative of log|z|.
    if u.imag.is_zero():return enclosed_G(u.real)
    assert not u.imag.contains(0), 'uncertain root type'
    return (u*u*(u.log()/2-acb(3)/4)).real

def horner(c,x):
    out=arb(0)
    for a in reversed(c):out=out*x+a
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('cert');ap.add_argument('--output');ap.add_argument('--beat',default='1.8076686');ap.add_argument('--limit-cells',type=int,default=0);a=ap.parse_args()
    st=time.time();raw=open(a.cert,'rb').read();c=json.loads(raw)
    E=list(map(rat,c['edges']));D=list(map(rat,c['node_densities']));B=list(map(rat,c['b']));A=c['A']
    assert len(E)==len(D) and len(B)==len(A) and D[0]==D[-1]==0
    assert all(x<y for x,y in zip(E,E[1:])) and all(x>=0 for x in D+B)
    on=[i for i in range(len(D)-1) if D[i]>0 or D[i+1]>0];assert on and E[on[0]]>0
    assert all(E[i+1]-E[i]<1 for i in on)
    mass=sum(((D[i]+D[i+1])*(E[i+1]-E[i])/2 for i in on),Q(0));trace=sum(((E[i+1]-E[i])*((2*E[i]+E[i+1])*D[i]+(E[i]+2*E[i+1])*D[i+1])/6 for i in on),Q(0))
    assert trace/mass==rat(c['bound']);assert sum(b*(len(q)-1) for b,q in zip(B,A))<mass
    roots=[];seen=set()
    for q in A:
        assert all(type(v) is int for v in q) and q[-1]>0 and len(q)>1
        assert tuple(q) not in seen;seen.add(tuple(q));p=fmpz_poly(q);unit,fac=p.factor()
        assert abs(unit)==1 and len(fac)==1 and fac[0][1]==1 and fac[0][0].degree()==p.degree()
        rr=[]
        for z,m in p.complex_roots():
            assert m==1
            assert z.imag.is_zero() or not z.imag.contains(0)
            rr.append(z)
        assert len(rr)==p.degree();roots.append(rr)
    EB=list(map(ball,E));DB=list(map(ball,D));BB=list(map(ball,B))
    slopes=[(D[i+1]-D[i])/(E[i+1]-E[i]) for i in range(len(D)-1)]
    sp=[Q(0)]+slopes+[Q(0)]
    jumps=[(e,ball(sp[k+1]-sp[k])) for k,e in enumerate(E) if sp[k+1]!=sp[k]]
    moments=[]
    for q,rr in zip(A,roots):
        val=ball(mass)*arb(q[-1]).log()
        for e,jump in jumps:
            val+=jump*sum((root_primitive(r-acb(ball(e))) for r in rr),arb(0))
        assert val>0,('E4 failed',val);moments.append(float(val.lower()))
    print('E1-E4 and E6 pass', 'bound',float(trace/mass),'min integral',min(moments),flush=True)
    # jumps were formed exactly from the piecewise linear density slopes
    rootterms=[(r,b) for rr,b in zip(roots,BB) for r in rr]
    leading_term=sum((b*arb(q[-1]).log() for q,b in zip(A,BB)),arb(0))
    pieces=0;worst=math.inf;maxdepth=0
    for n,i in enumerate(on):
        left,right=E[i:i+2];mid=(left+right)/2;rho=(right-left)/2;M=ball(mid);R=ball(rho)
        coeff=[-leading_term]+[arb(0) for _ in range(ORDER)];tail=arb(0);near_edges=[];near_roots=[]
        for e,jump in jumps:
            u=M-ball(e)
            if abs(u)>4*R:
                coeff[0]+=jump*G(u);coeff[1]+=jump*u*(abs(u).log()-1);coeff[2]+=jump*abs(u).log()/2
                inv=1/u;power=inv
                for k in range(3,ORDER+1):
                    coeff[k]+=jump*((-1)**(k-3))*power/(k*(k-1)*(k-2));power*=inv
                t=R/abs(u)
                tail+=abs(jump*u*u)*t**(ORDER+1)/((ORDER+1)*ORDER*(ORDER-1)*(1-t))
            else:near_edges.append((e,jump))
        for root,b in rootterms:
            u=M-root
            if abs(u)>4*R:
                coeff[0]-=b*abs(u).log();power=arb(1);inv=1/u
                for k in range(1,ORDER+1):
                    power*=inv;coeff[k]+=(b*((-1)**k)*power/k).real
                t=R/abs(u);tail+=b*t**(ORDER+1)/((ORDER+1)*(1-t))
            else:near_roots.append((root,b))
        c1=[k*coeff[k] for k in range(1,ORDER+1)];c2=[k*(k-1)*coeff[k] for k in range(2,ORDER+1)]
        stack=[(left,right,0)]
        while stack:
            s,t,depth=stack.pop();m=(s+t)/2;r=(t-s)/2;mb=ball(m);rb=ball(r);z=ball(m-mid);Z=ball(s-mid).union(ball(t-mid))
            v=horner(coeff,z);slope=horner(c1,z);curv=horner(c2,Z)/2;v-=tail.upper()
            for e,jump in near_edges:
                u=ball(m-e);X=ball(s-e).union(ball(t-e))
                if s==e or t==e:
                    # e is an endpoint: sign of G'' is constant in this cell.
                    if jump<0:
                        v+=jump*G(u);slope+=jump*u*(abs(u).log()-1)
                    else:
                        fs=jump*G(ball(s-e));ft=jump*G(ball(t-e))
                        v+=(fs+ft)/2;slope+=(ft-fs)/ball(t-s)
                else:
                    assert not X.contains(0)
                    v+=jump*G(u);slope+=jump*u*(abs(u).log()-1);curv+=jump*abs(X).log()/2
            for root,b in near_roots:
                X=ball(s).union(ball(t))-root;u=mb-root
                if not X.contains(0):
                    v-=b*abs(u).log();slope-=(b/u).real;curv+=(b/(X*X)/2).real
                else:
                    distance=abs(X).upper();assert distance>0
                    v-=b*distance.log()
            cl=curv.lower();lb=(v-abs(slope)*rb+min(arb(0),cl)*rb**2).lower()
            if cl>0:
                lb=max(lb,(v-slope**2/(4*cl)).lower())
            if lb>0:
                pieces+=1;worst=min(worst,float(lb));maxdepth=max(maxdepth,depth)
            else:
                if depth>=16:
                    point=sum((jump*G(ball(m-e)) for e,jump in jumps),arb(0))-leading_term
                    for root,b in rootterms:
                        dist=abs(mb-root)
                        if dist.contains(0):point=arb('inf');break
                        point-=b*dist.log()
                    assert not point<0,('E5 counterexample',str(m),str(point))
                assert depth<42,('E5 unresolved',i,s,t,lb)
                stack.extend([(s,m,depth+1),(m,t,depth+1)])
        if (n+1)%100==0:print('cells',n+1,'/',len(on),'pieces',pieces,'seconds',round(time.time()-st,1),flush=True)
        if a.limit_cells and n+1>=a.limit_cells:raise SystemExit('PARTIAL ONLY')
    result=dict(valid=True,certificate_sha256=hashlib.sha256(raw).hexdigest(),bound=str(trace/mass),bound_float=float(trace/mass),beats=trace/mass<rat(a.beat),threshold=a.beat,min_E4=min(moments),pieces=pieces,min_E5_lower=worst,maxdepth=maxdepth,seconds=time.time()-st)
    print(json.dumps(result,indent=2));
    if a.output:open(a.output,'w').write(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
