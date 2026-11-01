#!/usr/bin/env python3
"""Independent C86 checker, written from PROOF.md and mathematics only.

No target/search/checker imports. Execute on the authorized CPU pod only.
All acceptance decisions use Fraction arithmetic or Arb strict inequalities.
Float output is diagnostic only. See VERIFIER_NOTES.md for the enclosures.
"""
import argparse
import hashlib
import json
import math
import time
from fractions import Fraction as F
from pathlib import Path
from flint import arb, acb, fmpz_poly, ctx

if not __debug__:
    raise SystemExit('Refusing python -O: certificate assertions must remain enabled.')

ctx.prec = 192

def B(q):
    q = F(q)
    return arb(q.numerator) / q.denominator

def symmetric(r):
    return arb(0, r.abs_upper())

def primitive_real(t):
    if t.is_zero():
        return arb(0)
    assert not t.contains(0), 'ambiguous endpoint/root coincidence'
    return t*t*(abs(t).log()/2 - B(F(3,4)))

def primitive_complex(z):
    if z.imag.is_zero():
        return primitive_real(z.real)
    assert not z.imag.contains(0), 'uncertified real/nonreal classification'
    return (z*z*(z.log()/2 - B(F(3,4)))).real

def load_certificate(path):
    raw = Path(path).read_bytes()
    c = json.loads(raw)
    e = list(map(F, c['edges']))
    h = list(map(F, c['node_densities']))
    a = c['A']
    b = list(map(F, c['b']))
    assert len(e) == len(h) >= 2
    assert all(x < y for x,y in zip(e,e[1:])), 'edge ordering'
    assert e[0] > 0 and all(y >= 0 for y in h), 'positive real support/density'
    assert h[0] == h[-1] == 0, 'continuous zero extension required'
    assert len(a) == len(b) > 0 and all(x > 0 for x in b), 'active weights'
    assert len(set(map(tuple,a))) == len(a), 'duplicate auxiliaries'
    mass = F(0); trace = F(0); slopes=[]; cells=[]
    for i,(x,y,u,v) in enumerate(zip(e,e[1:],h,h[1:])):
        w=y-x
        mass += w*(u+v)/2
        trace += w*((2*x+y)*u+(x+2*y)*v)/6
        slopes.append((v-u)/w)
        if u or v:
            cells.append(i)
    assert mass > 0
    bound=F(c['bound'])
    assert bound == trace/mass, 'incorrect declared bound'
    assert bound > F('1.80220'), 'violates known lower bound: investigate'
    degree=F(0); roots=[]; integral_records=[]
    for p,w in zip(a,b):
        assert all(type(k) is int for k in p) and len(p)>=2 and p[-1]>0
        assert math.gcd(*p)==1, 'nonprimitive auxiliary'
        poly=fmpz_poly(p)
        content,factors=poly.factor()
        assert content==1 and len(factors)==1 and factors[0][0]==poly and factors[0][1]==1, 'reducible auxiliary'
        rr=poly.complex_roots()
        assert sum(mult for _,mult in rr)==len(p)-1 and all(mult==1 for _,mult in rr)
        assert len(rr)==len(p)-1
        for root,_ in rr:
            roots.append((root,B(w)))
        degree += w*(len(p)-1)
        integral_records.append((p,w,[r for r,_ in rr]))
    assert degree < mass, 'weighted-degree inequality'
    jumps=[slopes[0]]+[v-u for u,v in zip(slopes,slopes[1:])]+[-slopes[-1]]
    # These identities also catch sign/index errors in the potential primitive.
    assert sum(jumps)==0
    assert sum(j*x for j,x in zip(jumps,e))==0
    assert sum(j*x*x/2 for j,x in zip(jumps,e))==mass
    terms=[(x,j,B(x),B(j)) for x,j in zip(e,jumps) if j]
    return dict(c=c,edges=e,heights=h,mass=mass,trace=trace,bound=bound,
                degree=degree,roots=roots,records=integral_records,cells=cells,
                terms=terms,sha256=hashlib.sha256(raw).hexdigest())

def potential(data,z):
    z=acb(z)
    return sum((jb*primitive_complex(z-eb) for _,_,eb,jb in data['terms']),arb(0))

def point_gap(data,x):
    z=acb(B(x))
    ans=potential(data,z)
    for p,w,_ in data['records']:
        value=acb(0)
        for k in reversed(p):
            value=value*z+k
        assert abs(value)>0
        ans -= B(w)*abs(value).log()
    return ans

def cell_integral(data,root):
    # Direct primitive per density segment, separate from the jump formula.
    # rho(x)=s*(x-root)+rho(root), with complex rho(root).
    total=arb(0)
    e=data['edges']; h=data['heights']
    def anti(z,s,k):
        if z.imag.is_zero():
            t=z.real
            if t.is_zero():return arb(0)
            assert not t.contains(0)
            return (s*t*t/2+k.real*t)*abs(t).log()-s*t*t/4-k.real*t
        assert not z.imag.contains(0)
        return ((s*z*z/2+k*z)*z.log()-s*z*z/4-k*z).real
    for i in data['cells']:
        x,y=e[i:i+2]; u,v=h[i:i+2]
        s=B((v-u)/(y-x)); k=B(u)+s*(root-B(x))
        total += anti(B(y)-root,s,k)-anti(B(x)-root,s,k)
    return total

def check_integrals(data):
    output=[]
    for idx,(p,w,rr) in enumerate(data['records']):
        direct=B(data['mass'])*B(p[-1]).log()
        by_jumps=direct
        for root in rr:
            direct += cell_integral(data,root)
            by_jumps += potential(data,root)
        assert (direct-by_jumps).contains(0), 'primitive cross-check'
        assert direct>0, f'negative/uncertain log integral {idx}: {direct}'
        row={'index':idx,'coefficients':p,'enclosure':str(direct),
             'lower':str(direct.lower()),'nonreal_roots':sum(not r.imag.is_zero() for r in rr)}
        output.append(row)
        print('INTEGRAL',idx,direct,flush=True)
    return output

def interval_gap(data,left,right,order=8):
    """Taylor enclosure, with an integrable-log bound at density knots.

    Closed rational [left,right] is covered; no floating interval endpoints.
    For near knots use concavity of G''=log|t| on |t|<1 and
    |G(t+h)-G(t)-hG'(t)| <= 2*r^2*(1-log r).
    Far terms use a Lagrange remainder with the exact minimum distance.
    """
    center=(left+right)/2; radius=(right-left)/2
    assert radius>0 and radius<F(1,10)
    cb=B(center); rb=B(radius)
    coeff=[arb(0) for _ in range(order+1)]
    error=arb(0)
    for edge,jump,eb,jb in data['terms']:
        t=center-edge; tb=B(t)
        if t:
            logt=abs(tb).log()
            coeff[0]+=jb*tb*tb*(logt/2-B(F(3,4)))
            coeff[1]+=jb*tb*(logt-1)
        if abs(t)<=2*radius:
            assert abs(t)+radius<1
            if jump>0:
                error+=jb*2*rb*rb*(1-rb.log())
        else:
            coeff[2]+=jb*logt/2
            cn=jb/(6*tb)
            for n in range(3,order+1):
                coeff[n]+=cn
                cn=-cn*(n-2)/((n+1)*tb)
            dist=B(abs(t)-radius)
            error+=abs(jb)*rb**(order+1)/((order+1)*order*(order-1)*dist**(order-1))
    for p,w,_ in data['records']:
        coeff[0]-=B(w)*B(p[-1]).log()
    for root,weight in data['roots']:
        z=acb(cb)-root
        distance=abs(z)
        if distance>2*rb:
            coeff[0]-=weight*distance.log()
            iz=1/z
            power=iz
            for n in range(1,order+1):
                coeff[n]-=weight*((-1)**(n+1))*power.real/n
                power*=iz
            ratio=rb/distance
            error+=weight*ratio**(order+1)/((order+1)*(1-ratio))
        else:
            # Supremum distance gives a valid lower bound, even at a root.
            coeff[0]-=weight*(distance+rb).log()
    hball=symmetric(rb)
    value=coeff[-1]
    for v in reversed(coeff[:-1]):
        value=value*hball+v
    return value-error

def verify(path,output,order=8,maxdepth=32,only_integrals=False,witness=None):
    started=time.time();data=load_certificate(path)
    receipt={k:str(data[k]) for k in ['mass','trace','bound','degree','sha256']}
    receipt['nodes']=len(data['edges']);receipt['support_cells']=len(data['cells'])
    print('EXACT',receipt,flush=True)
    if witness is not None:
        value=point_gap(data,F(witness));print('WITNESS',witness,value,flush=True)
        assert value>0, 'nonpositive potential witness'
        return
    receipt['integrals']=check_integrals(data)
    if only_integrals:
        Path(output).write_text(json.dumps(receipt,indent=2));return
    cover=[];tests=0;min_lower=None;max_depth=0
    for cell in data['cells']:
        e=data['edges'];stack=[(e[cell],e[cell+1],0)];accepted=[]
        while stack:
            lo,hi,depth=stack.pop();tests+=1
            enclosure=interval_gap(data,lo,hi,order)
            if enclosure>0:
                lower=enclosure.lower()
                if min_lower is None or lower<min_lower:min_lower=lower
                accepted.append((lo,hi))
                cover.append([cell,str(lo),str(hi),str(lower)])
                max_depth=max(max_depth,depth)
            else:
                mid=(lo+hi)/2
                point=point_gap(data,mid)
                assert not point<0, f'negative potential at {mid}: {point}'
                assert depth<maxdepth, f'unresolved cell {cell} [{lo},{hi}]: {enclosure}'
                stack.append((mid,hi,depth+1));stack.append((lo,mid,depth+1))
        # Independent exact coverage audit for every original support cell.
        accepted.sort()
        assert accepted[0][0]==e[cell] and accepted[-1][1]==e[cell+1]
        assert all(u[1]==v[0] for u,v in zip(accepted,accepted[1:])), 'coverage gap'
        if cell%40==0:
            print('COVER',cell,'tests',tests,'pieces',len(cover),'min',min_lower,'seconds',round(time.time()-started,1),flush=True)
            Path(str(output)+'.progress').write_text(json.dumps({'cell':cell,'pieces':len(cover),'seconds':time.time()-started}))
    receipt.update(status='PASS',pieces=len(cover),tests=tests,max_depth=max_depth,
                   minimum_proven_lower=str(min_lower),seconds=time.time()-started,
                   support_left=str(data['edges'][data['cells'][0]]),
                   support_right=str(data['edges'][data['cells'][-1]+1]),
                   precision_bits=ctx.prec,order=order)
    coverage_path=Path(str(output)+'.cover.json')
    coverage_path.write_text(json.dumps(cover,separators=(',',':')))
    receipt['coverage_sha256']=hashlib.sha256(coverage_path.read_bytes()).hexdigest()
    Path(output).write_text(json.dumps(receipt,indent=2))
    print('PASS',json.dumps({k:v for k,v in receipt.items() if k!='integrals'}),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate');parser.add_argument('--output',default='receipt.json')
    parser.add_argument('--order',type=int,default=8);parser.add_argument('--maxdepth',type=int,default=32)
    parser.add_argument('--integrals-only',action='store_true');parser.add_argument('--witness')
    args=parser.parse_args()
    verify(args.certificate,args.output,args.order,args.maxdepth,args.integrals_only,args.witness)
