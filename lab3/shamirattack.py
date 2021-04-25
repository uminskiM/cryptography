import numpy as np
import sympy as sp
from bitstring import xrange
from numpy.compat import long
from sympy import *
from fractions import *
from itertools import combinations
from math import *
import time
from random import shuffle

def build_in(aa, N):
    n = len(aa)
    for i in xrange(n):
        aa[i] = Fraction(aa[i])
    A = sp.zeros(2 * n - 1, n)
    b = sp.zeros(2 * n - 1, 1)
    c = sp.zeros(2 * n - 1, 1)
    for i in xrange(n - 1):
        A[i, 0] = aa[i + 1]
        A[i, i + 1] = -aa[0]
        b[i, 0] = Fraction(aa[0] * aa[i + 1], 2 ** (3 * N - 1 - i))
        c[i, 0] = 0
    for i in xrange(n):
        A[n + i - 1, i] = 1
        b[n + i - 1] = aa[i] - 1
        c[n + i - 1] = 1
    # print A
    # print b
    # print c
    return (A, b, c)


def face_enumerator(b, c, depth=0, d=0):
    n = b.shape[0]
    if (depth == 0):
        d = sp.zeros(n, 1)
    if (depth == n):
        yield d
    else:
        d[n - 1 - depth, 0] = c[n - 1 - depth, 0]
        fe = face_enumerator(b, c, depth + 1, d)
        for f in fe:
            yield f
        if (b[n - 1 - depth, 0] != c[n - 1 - depth, 0]):
            d[n - 1 - depth, 0] = b[n - 1 - depth, 0]
            fe = face_enumerator(b, c, depth + 1, d)
            for f in fe:
                yield f


def check(A, b, c, v):
    m = A.shape[0]
    w = A * v
    for i in xrange(m):
        if (b[i, 0] < w[i, 0] or w[i, 0] < c[i, 0]):
            return False
    return True

def delete_useless_rows(A, b, c):
    nA = A[:, :]
    nb = b[:, :]
    nc = c[:, :]
    nm = 0
    m = A.shape[0]
    n = A.shape[1]
    for i in xrange(m):
        if (A[i, :] == -A[i, :]):
            if (b[i, 0] < 0 or 0 < c[i, 0]):
                return (False, A, b, c)
            else:
                continue
        else:
            k = -1
            for j in xrange(n):
                if (A[i, j] != 0):
                    k = j
                    break
            flag = True
            for j in xrange(nm):
                r = nA[j, k] / A[i, k]
                if (nA[j, :] == A[i, :] * r):
                    nbb = b[i, 0] * r
                    ncc = c[i, 0] * r
                    if (r < 0):
                        nbb, ncc = ncc, nbb
                    nb[j, 0] = min(nb[j, 0], nbb)
                    nc[j, 0] = max(nc[j, 0], ncc)
                    if (nb[j, 0] < nc[j, 0]):
                        return (False, A, b, c)
                    flag = False
                    break
            if (flag):
                nA[nm, :] = A[i, :]
                nb[nm, 0] = b[i, :]
                nc[nm, 0] = c[i, :]
                if (nb[nm, 0] < nc[nm, 0]):
                    return (False, A, b, c)
                nm += 1
    return (True, nA[:nm, :], nb[:nm, :], nc[:nm, :])

def get_vertices_boost(A, b, c):
    vs = []
    m = A.shape[0]
    n = A.shape[1]
    used = np.zeros((m, 1))
    rowlist = range(n - 1)
    for lastrow in xrange(n - 1, m):
        lrowlist = list(rowlist)
        lrowlist.append(lastrow)
        subA = A.extract(lrowlist, range(n))
        if (subA.det() != 0):
            iA = subA.inv()
            subb = b.extract(lrowlist, [0])
            subc = c.extract(lrowlist, [0])
            faces = face_enumerator(subb, subc)
            for subd in faces:
                v = iA * subd
                if (check(A, b, c, v)):
                    vs.append(v)
                    for i in lrowlist:
                        used[i, 0] = 1
    important = []
    for i in xrange(m):
        if (used[i, 0] != 0):
            important.append(i)
    return (vs, important)

def get_vertices(A, b, c):
    vs = []
    m = A.shape[0]
    n = A.shape[1]
    used = np.zeros((m, 1))
    for rowlist in combinations(range(m), n):
        lrowlist = list(rowlist)
        subA = A.extract(rowlist, range(n))
        if (subA.det() != 0):
            iA = subA.inv()
            subb = b.extract(rowlist, [0])
            subc = c.extract(rowlist, [0])
            faces = face_enumerator(subb, subc)
            for subd in faces:
                v = iA * subd
                if (check(A, b, c, v)):
                    vs.append(v)
                    for i in lrowlist:
                        used[i, 0] += 1
    important = []
    for i in xrange(m):
        if (used[i, 0] != 0):
            important.append(i)
    return (vs, important)

def regular_simplex(n):
    RS = sp.Matrix([[1, 0, 0, 0],
                    [0, Fraction(13, 15), 0, 0],
                    [0, 0, Fraction(40, 49), 0],
                    [0, 0, 0, Fraction(15, 19)]])
    for i in xrange(n):
        for j in xrange(i + 1, n):
            RS[i, j] = RS[i, i] / (i + 2)
    RS = RS[:n, :n]
    x = RS[:n, (n - 1)]
    x[(n - 1), 0] /= (n + 1)
    return (RS, x)


def get_simplex(A, b, c, vs):
    n = vs[0].shape[0]
    nv = len(vs)

    V = sp.zeros(n, nv)
    for i in xrange(nv):
        V[:, i] = vs[i]
    S = V[:, 1:]
    v0 = V[:, 0]
    for i in xrange(nv - 1):
        S[:, i] -= v0

    dim = 0
    cols = []
    used = sp.zeros(nv - 1, 1)
    j = 1
    while (j < nv):
        i = j - 1
        used[i] = 1
        cols.append(i)
        dim += 1
        if (dim > S.extract(range(n), cols).rank()):
            del cols[-1]
            dim -= 1
        if (dim == n):
            break
        j *= 2
    if (dim != n):
        for i in xrange(nv - 1):
            if (used[i] == 1):
                continue
            used[i] = 1
            cols.append(i)
            dim += 1
            if (dim > S.extract(range(n), cols).rank()):
                del cols[-1]
                dim -= 1
            if (dim == n):
                break
    Simplex = S.extract(range(n), cols)
    return (Simplex, v0, S, cols)


def get_endomorphism(A, b, c, Simplex, v0, S, cols):
    n = A.shape[1]
    nv = S.shape[1] + 1
    Si = Simplex.inv()
    while (True):
        Vol = Si * S
        mi = 0
        mj = 0
        for i in xrange(n):
            for j in xrange(nv - 1):
                if (abs(Vol[i, j]) > abs(Vol[mi, mj])):
                    mi = i
                    mj = j
        if (abs(Vol[mi, mj]) > Fraction(3, 2)):
            cols[mi] = mj
            Simplex[:, mi] = S[:, mj]
            Si = Simplex.inv()
        else:
            break
    v1 = v0
    for i in xrange(n):
        v1 += Simplex.col(i)
    RS = Matrix([0])
    x = Matrix([0])
    if (check(A, b, c, v1)):
        RS = sp.eye(n)
        x = Fraction(1, 2) * sp.ones(n, 1)
    else:
        (RS, x) = regular_simplex(n)

    M = RS * Si
    x += M * v0
    return (M, x)


def reduce_mu(U, Mu, k, l):
    mkl = Mu[k, l]
    if (abs(mkl) > Fraction(1, 2)):
        r = long(round(mkl))
        U[:, k] -= r * U[:, l]
        for j in xrange(l):
            Mu[k, j] -= r * Mu[l, j]
        Mu[k, l] -= r


def reduce_basis(U):
    U = U[:, :]
    n = U.shape[0]

    Mu = sp.zeros(n)
    Bs = sp.zeros(n)
    Bj = sp.zeros(n, 1)

    for i in xrange(n):
        Bs[:, i] = U[:, i]
        for j in xrange(i):
            Mu[i, j] = U.col(i).dot(Bs.col(j)) / Bj[j, 0]
            Bs[:, i] -= Bs[:, j] * Mu[i, j]
        Bj[i, 0] = Bs.col(i).dot(Bs.col(i))

    k = 1
    while (k < n):
        reduce_mu(U, Mu, k, k - 1)
        if (Bj[k, 0] < (Fraction(3, 4) - Mu[k, k - 1] ** 2) * Bj[k - 1, 0]):
            mu = Mu[k, k - 1]
            B = Bj[k, 0] + mu ** 2 * Bj[k - 1, 0]
            Mu[k, k - 1] = mu * Bj[k - 1, 0] / B
            Bj[k, 0] = Bj[k - 1, 0] * Bj[k, 0] / B
            Bj[k - 1, 0] = B
            U[:, k - 1], U[:, k] = U[:, k], U[:, k - 1]

            cs = Bs[:, k] + mu * Bs[:, (k - 1)]  # !!!!!
            Bs[:, k] = Bs[:, (k - 1)] - Mu[k, k - 1] * cs
            Bs[:, (k - 1)] = cs

            for j in xrange(k - 1):
                Mu[k - 1, j], Mu[k, j] = Mu[k, j], Mu[k - 1, j]
            T = Matrix([[1, Mu[k, k - 1]], [0, 1]]) * Matrix([[0, 1], [1, -mu]])
            for i in xrange(k + 1, n, 1):
                TT = Matrix([[Mu[i, k - 1]], [Mu[i, k]]])
                TT = T * TT
                Mu[i, k - 1] = TT[0, 0]
                Mu[i, k] = TT[1, 0]
            if (k > 1):
                k -= 1
        else:
            for l in xrange(k - 2, -1, -1):
                reduce_mu(U, Mu, k, l)
            k += 1

    mi = (n - 1)
    m = 0
    for i in xrange(n - 1, -1, -1):
        t = U.col(i).dot(U.col(i))
        if (t > m):
            mi = i
            m = t

    if (n - 1 != mi):
        U[:, (n - 1)], U[:, mi] = U[:, mi], U[:, (n - 1)]
        for i in xrange(n):
            Bs[:, i] = U[:, i]
            for j in xrange(i):
                if (n - 1 != mi):
                    Mu[i, j] = U.col(i).dot(Bs.col(j)) / Bj[j, 0]
                Bs[:, i] -= Bs[:, j] * Mu[i, j]
            Bj[i, 0] = Bs.col(i).dot(Bs.col(i))
    return (U, Bs, Bj)


def make_integer_matrix(A):
    A = A[:, :]
    n = A.shape[0]
    m = A.shape[1]
    for j in xrange(m):
        p = Fraction(1)
        for i in xrange(n):
            t = Fraction(str(A[i, j])).denominator
            g = gcd(t, p)
            p *= t / g
        A[:, j] *= p
    return A


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return (gcd, x, y)


def diagonal_reduce(A, K, j):
    if (A[j, j] < 0):
        A[:, j] *= -1
        K[:, j] *= -1
        for i in xrange(j):
            r = long(ceil(A[j, i] / A[j, j]))
            K[:, i] -= r * K[:, j]
            A[:, i] -= r * A[:, j]


def HNF(A):
    A = A[:, :]
    A = A.T
    n = A.shape[1]
    m = A.shape[0]
    K = sp.eye(n)

    cols = []
    for i in xrange(n):
        if (i < m):
            for j in xrange(i, n):
                cols.append(j)
                if (A.extract(range(i + 1), cols).det() == 0):
                    del cols[-1]
                else:
                    A[:, i], A[:, j] = A[:, j], A[:, i]
                    K[:, i], K[:, j] = K[:, j], K[:, i]
                    cols[-1] = i
                    break
        for j in xrange(min(i, m)):
            (r, p, q) = egcd(A[j, j], A[j, i])
            p1 = -A[j, i] / r
            q1 = A[j, j] / r
            a1, a2 = A[:, j], A[:, i]
            k1, k2 = K[:, j], K[:, i]
            A[:, j] = p * a1 + q * a2
            K[:, j] = p * k1 + q * k2
            A[:, i] = p1 * a1 + q1 * a2
            K[:, i] = p1 * k1 + q1 * k2
            diagonal_reduce(A, K, j)
        if (i < m):
            diagonal_reduce(A, K, i)
    return (K.T, A.T)


def Lenstra_anchor(A, b, c):
    m = A.shape[0]
    l = 0
    r = 0
    flag = True
    for i in xrange(m):
        a = A[i, 0]
        if (a != 0):
            nr = b[i, 0] / a
            nl = c[i, 0] / a
            if (a < 0):
                nr, nl = nl, nr
            if (flag):
                r = nr
                l = nl
                flag = False
            else:
                r = min(r, nr)
                l = max(l, nl)
            if (not flag and r < l):
                return (False, [])
        else:
            if (0 <= b[i, 0] and c[i, 0] <= 0):
                continue
            else:
                return (False, [])
    l = long(ceil(l))
    r = long(floor(r))

    ans = []  # !!!
    while (l <= r):
        ans.append(Matrix([[l]]))
        l += 1
    return (True, ans)

    if (l <= r):
        return (True, [Matrix([[l]])])
    else:
        return (True, [])


def Lenstra(A, b, c, boost=False):
    A = A[:, :]
    b = b[:, :]
    c = c[:, :]
    n = A.shape[1]

    if (n == 1):
        return Lenstra_anchor(A, b, c)

    if (boost):
        (vs, important) = get_vertices_boost(A, b, c)
    else:
        (flag, A, b, c) = delete_useless_rows(A, b, c)
        if (flag == False):
            return (False, [])
        (vs, important) = get_vertices(A, b, c)

    if (len(vs) == 0):
        return (False, [])

    A = A.extract(important, range(n))
    b = b.extract(important, [0])
    c = c.extract(important, [0])
    (Simplex, v0, S, cols) = get_simplex(A, b, c, vs)

    if (Simplex.shape[1] < n):
        dim = Simplex.shape[1]
        W = make_integer_matrix(Simplex)
        (U, K) = HNF(W)
        Ui = U.inv()
        res = U * v0
        for i in xrange(dim, n):
            r = long(round(res[i, 0]))
            if (r != res[i, 0]):
                return (False, [])
        nA = A * Ui
        nb = b[:, 0]
        nc = c[:, 0]
        for i in xrange(dim, n):
            nb -= res[i, 0] * nA[:, i]
            nc -= res[i, 0] * nA[:, i]
        nA = nA[:, :dim]
        (flag, lst) = Lenstra(nA, nb, nc)
        if (flag == False):
            return (False, [])
        else:  # !!!
            ans = []
            for y in lst:
                res[:dim, 0] = y
                ans.append(Ui * res)
        return (True, ans)

    (M, x) = get_endomorphism(A, b, c, Simplex, v0, S, cols)
    nA = A * M.inv()

    (U, Bs, B) = reduce_basis(M)
    nA = nA * U
    m = nA.shape[0]
    n = nA.shape[1]

    res = sp.zeros(n, 1)
    for i in xrange(n - 1, -1, -1):
        r = x.dot(Bs.col(i)) / B[i, 0]
        cr = long(round(r))
        x -= cr * U.col(i)
        r -= cr
        x -= r * Bs.col(i)
        res[i, 0] = cr
        break  # !!!

    MiU = M.inv() * U
    if (False):  # and check(nA, b, c, res)):
        return (True, [MiU * res])
    else:
        p = res[n - 1, 0]
        v = nA[:, n - 1]
        nA = nA[:, :(n - 1)]
        b -= v * p
        c -= v * p
        (flag, lst) = Lenstra(nA, b, c)
        ans = []
        if (flag == False):
            return (False, [])
        else:
            for y in lst:
                res[:(n - 1), 0] = y
                ans.append(MiU * res)
            flagP = True
            flagN = True
            i = 1
            while (flagP or flagN):
                nv = v * i
                if (flagP):
                    (flag, lst) = Lenstra(nA, b - nv, c - nv)
                    if (flag == False):
                        flagP = False
                    else:
                        res[(n - 1), 0] = p + i
                        for y in lst:
                            res[:(n - 1), 0] = y
                            ans.append(MiU * res)
                if (flagN):
                    (flag, lst) = Lenstra(nA, b + nv, c + nv)
                    if (flag == False):
                        flagN = False
                    else:
                        res[(n - 1), 0] = p - i
                        for y in lst:
                            res[:(n - 1), 0] = y
                            ans.append(MiU * res)
                i += 1
        return (True, ans)

def unique(lst):
    ans = []
    first = True
    for l in lst:
        if (first or ans[-1] != l):
            ans.append(l)
            first = False
    return ans



def solve(aa, ind, x1):
    a1 = aa[ind]

    l = x1 / a1
    r = (x1 + 1) / a1
    xx = []
    suma = Rational(0)
    sumx = Rational(0)
    for a in aa:
        nx = long(floor(x1 / a1 * a))
        nr = Rational(nx + 1) / a
        if (nr < r):
            r = nr
        suma += a
        sumx += nx
        xx.append(nx)
    maxr = (1 + sumx) / suma
    if (maxr <= l):
        return []
    r = min(r, maxr)

    tt = [l]
    cl = len(aa)
    for i in xrange(cl):
        for j in xrange(i + 1, cl):
            t = Rational(xx[i] - xx[j]) / (aa[i] - aa[j])
            if (l < t and t < r):
                tt.append(t)
    start = time.clock()
    tt.append(r)
    tt.sort()
    tt = unique(tt)
    np = len(tt)
    sl = tt[0]
    perm = []
    for i in xrange(cl):
        perm.append(i)

    ans = []
    for i in xrange(1, np):
        sr = tt[i]
        sm = (sr + sl) / 2
        perm.sort(key=lambda x: (aa[x] * sr - xx[x]))
        suma = Rational(aa[perm[0]])
        sumx = Rational(xx[perm[0]])
        nl = sl
        nr = sr
        for j in xrange(1, cl):
            ai = aa[perm[j]]
            xi = xx[perm[j]]
            if (suma == ai):
                if (sumx - xi <= 0):
                    nr = nl - 1
                    break
            else:
                if (suma > ai):
                    nr = min(nr, (sumx - xi) / (suma - ai))
                else:
                    nl = max(nl, (sumx - xi) / (suma - ai))
                if (nr <= nl):
                    break
            suma += ai
            sumx += xi
        nr = min(nr, maxr)
        if (nl < nr):
            ans.append((nl, nr))
        sl = sr
    return ans

def Shamir_attack(aa):
    N = 0
    N2 = 1
    for a in aa:
        while (N2 < a):
            N += 1
            N2 *= 2
    N = N / 2

    n = 4
    cn = len(aa)
    for i in xrange(cn):
        for j in xrange(cn):
            if (j == i):
                continue
            for k in xrange(cn):
                if (k == j or k == i):
                    continue
                for h in xrange(cn):
                    if (h == k or h == j or h == i):
                        continue
                    print
                    i, j, k, h
                    (A, b, c) = build_in([aa[i], aa[j], aa[k], aa[h]], N)
                    (flag, ans) = Lenstra(A, b, c, True)
                    print
                    len(ans)
                    for a in ans:
                        x = a[0]
                        segments = solve(aa, i, x)
                        if (len(segments) > 0):
                            ans = find_Wi_M(segments, N, aa)
                            if (len(ans) > 0):
                                return ans
                    # break
                # break
            # break
        # break


def find_Wi_M(segs, N, aa):
    ans = []
    for seg in segs:
        (l, r) = seg
        length = r - l
        cfl = to_cfraction(l)
        cfr = to_cfraction(r)
        cfm = []
        ncfl = len(cfl)
        ncfr = len(cfr)
        flag = True
        for i in xrange(min(ncfl, ncfr)):
            if (cfl[i] != cfr[i]):
                flag = False
                taill = cfl[i:]
                tailr = cfr[i:]
                if (cfl[i] > cfr[i]):
                    taill, tailr = tailr, taill
                if (len(tailr) > 1 or taill[0] + 1 < tailr[0]):
                    cfm.append(taill[0] + 1)
                    break
                else:
                    cfm.append(taill[0])
                    cfm.append(1)
                    break
            else:
                cfm.append(cfl[i])
        if (flag):
            if (ncfl < ncfr):
                cfm.append(cfr[ncfl])
            else:
                cfm.append(cfl[ncfr])
        ans.append(from_cfraction(cfm))
    return ans

def to_cfraction(x):
    ans = []
    while (True):
        n = long(floor(x))
        ans.append(n)
        x -= n
        if (x == 0):
            break
        x = 1 / x
    return ans

def from_cfraction(lst):
    x = Fraction(0)
    for d in reversed(lst):
        x += d
        x = 1 / x
    x = 1 / x
    return (x.numerator, x.denominator)


def read_public_key(filename):
    f = open(filename)
    i = 0
    for line in f:
        if (i == 1):
            vals = line[:].split(' ')[:(-1)]
        i += 1
    for i in xrange(len(vals)):
        vals[i] = long(vals[i])
    return vals


def time_test():
    f = open('loggy.txt', 'w')
    for n in xrange(8, 68, 4):
        sumt = 0
        for keynum in xrange(1, 4):
            print
            n, keynum
            name = 'key_p_' + str(n) + '_' + str(keynum)
            vals = read_public_key(name)

            N = 0
            N2 = 1
            for a in vals:
                while (N2 < a):
                    N += 1
                    N2 *= 2
            N = N / 2

            perm = range(n)
            sumtime = 0
            f.write(str(n))
            f.flush()
            for it in xrange(10):
                shuffle(perm)
                (A, b, c) = build_in([vals[perm[0]], vals[perm[1]], vals[perm[2]], vals[perm[3]]], N)
                start = time.clock()
                (flag, ans) = Lenstra(A, b, c, True)
                thistime = time.clock() - start
                print
                thistime,
                f.write("\t" + str(thistime))
                f.flush()
                sumtime += thistime
            sumtime /= 10
            sumt += sumtime
            print
            print
            sumtime
            f.write("\t" + str(sumtime) + "\n")
            f.flush()
        sumt /= 3
        print
        sumt
        f.write(str(sumt) + "\n")
        f.flush()

    f.close()


def test():
    time_test()
    # vals = read_public_key('key_p_8_00')
    # ans = Shamir_attack(vals)
    # print ans

Shamir_attack()