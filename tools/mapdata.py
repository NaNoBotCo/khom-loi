#!/usr/bin/env python3
"""mapdata.py — cuts the water, the airport and its runway out of Mot Dang's land.json
(OpenStreetMap contributors, ODbL, via Protomaps) for the drift map. Writes docs/map.json.

Run:  python3 tools/mapdata.py [krathong]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAND = os.path.join(HERE, "..", "..", "mot-dang", "assets", "sites", "city-live", "data", "land.json")
S, W, N, E = 18.66, 98.88, 18.95, 99.10


def dec(e, k):
    pts, a, b = [], e[0], e[1]
    pts.append((a / k, b / k))
    for i in range(2, len(e), 2):
        a += e[i]; b += e[i + 1]
        pts.append((a / k, b / k))
    return pts


def area(r):
    a = 0.0
    for (x0, y0), (x1, y1) in zip(r, r[1:] + r[:1]):
        a += x0 * y1 - x1 * y0
    return abs(a) / 2 * 111320 ** 2 * 0.946


def dp(pts, eps):
    """Douglas-Peucker in degrees."""
    if len(pts) < 3:
        return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    dx, dy = bx - ax, by - ay
    L = (dx * dx + dy * dy) ** .5 or 1e-12
    i, m = 0, -1
    for j in range(1, len(pts) - 1):
        x, y = pts[j]
        dd = abs(dy * (x - ax) - dx * (y - ay)) / L
        if dd > m:
            i, m = j, dd
    if m < eps:
        return [pts[0], pts[-1]]
    return dp(pts[:i + 1], eps)[:-1] + dp(pts[i:], eps)


def moat(r):
    return all(18.776 < la < 18.80 and 98.975 < ln < 98.998 for la, ln in r)


def main():
    d = json.load(open(LAND))
    k = d["scale"]
    out = {"source": d["source"], "bbox": [S, W, N, E], "water": [], "air": [], "runways": []}
    for cls in ("water", "air"):
        for poly in d["feats"].get(cls, []):
            rings = [dec(r, k) for r in poly]
            if not any(S < la < N and W < ln < E for r in rings for la, ln in r):
                continue
            if cls == "water":
                rings = [r for r in rings if area(r) > 40000 or moat(r)]
                if not rings:
                    continue
            rings = [dp(r, 0.00004) for r in rings]
            out[cls].append([[[round(la, 4), round(ln, 4)] for la, ln in r] for r in rings if len(r) >= 3])
    for la, ln, dla, dln in d["runways"]:
        la, ln = la / k, ln / k
        if S < la < N and W < ln < E:
            out["runways"].append([round(la, 5), round(ln, 5), round(la + dla / k, 5), round(ln + dln / k, 5)])
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "docs", "map.json")
    json.dump(out, open(dest, "w"), separators=(",", ":"))
    print(dest, len(out["water"]), "water", len(out["air"]), "air", len(out["runways"]), "runways", os.path.getsize(dest), "bytes")


if __name__ == "__main__":
    main()
