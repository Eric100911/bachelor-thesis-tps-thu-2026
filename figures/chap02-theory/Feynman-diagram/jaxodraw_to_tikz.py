#!/usr/bin/env python3
"""Convert the local JaxoDraw XML diagrams to cleaner TikZ sources.

The XML files store hand-drawn coordinates.  This helper keeps the original
geometry but adds two small cleanups that matter for thesis figures:

1. endpoints that are nearly identical are snapped to a common vertex;
2. endpoints close to a JaxoDraw blob are projected onto the blob boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot, sqrt
from pathlib import Path
import argparse
import xml.etree.ElementTree as ET


DEFAULT_SOURCES = ("DPS-1.xml", "DPS-2.xml", "SPS.xml", "TPS.xml")
STYLE_FILE = "feynman-diagram-style.tex"


@dataclass
class Element:
    kind: str
    points: list[tuple[float, float]]
    text: str = ""
    arrow: bool = False
    source_id: str = ""


def _number_from_setter(setter: ET.Element | None) -> float | None:
    if setter is None:
        return None
    int_node = setter.find(".//int")
    if int_node is not None and int_node.text is not None:
        return float(int_node.text)
    for obj_ref in setter.findall(".//object"):
        if obj_ref.get("idref") == "Integer0":
            return 0.0
    return None


def _points(obj: ET.Element) -> list[tuple[float, float]]:
    arrays: list[list[tuple[float, float]]] = []
    for point_array in obj.findall("./void[@property='points']"):
        pts: list[tuple[float, float]] = []
        for point in point_array.findall("./void"):
            x = None
            y = None
            for field in point.findall("./void[@class='java.awt.Point'][@method='getField']"):
                name = field.findtext("string")
                value = _number_from_setter(field.find("./void[@method='set']"))
                if name == "x":
                    x = value
                elif name == "y":
                    y = value
            if x is not None and y is not None:
                pts.append((x, y))
        if pts:
            arrays.append(pts)
    return arrays[0] if arrays else []


def _text(obj: ET.Element) -> str:
    node = obj.find("./void[@property='textString']/string")
    return "" if node is None or node.text is None else node.text


def _has_arrow(obj: ET.Element) -> bool:
    if obj.find("./void[@property='arrow']") is not None:
        return True
    paint_arrow = obj.find("./void[@property='paintArrow']/boolean")
    return paint_arrow is not None and paint_arrow.text == "true"


def parse_jaxodraw(path: Path) -> list[Element]:
    root = ET.parse(path).getroot()
    elements: list[Element] = []
    seen_blobs: set[tuple[float, float, float, float]] = set()
    for obj in root.findall(".//object"):
        cls = obj.get("class", "")
        if not cls.startswith("net.sf.jaxodraw.object"):
            continue
        class_name = cls.split(".")[-1]
        if class_name == "JaxoFLine":
            elements.append(Element("fermion", _points(obj), arrow=_has_arrow(obj), source_id=obj.get("id", "")))
        elif class_name == "JaxoGlLine":
            elements.append(Element("gluon", _points(obj), source_id=obj.get("id", "")))
        elif class_name == "JaxoBlob":
            pts = _points(obj)
            if len(pts) >= 2:
                key = tuple(round(v, 1) for point in pts[:2] for v in point)
                if key in seen_blobs:
                    continue
                seen_blobs.add(key)
            elements.append(Element("blob", pts, source_id=obj.get("id", "")))
        elif class_name == "JaxoLatexText":
            elements.append(Element("label", _points(obj), text=_text(obj), source_id=obj.get("id", "")))
    return elements


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return hypot(a[0] - b[0], a[1] - b[1])


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def snap_vertices(elements: list[Element], radius: float) -> None:
    endpoint_refs: list[tuple[Element, int, tuple[float, float]]] = []
    for element in elements:
        if element.kind in {"fermion", "gluon"} and len(element.points) >= 2:
            endpoint_refs.append((element, 0, element.points[0]))
            endpoint_refs.append((element, 1, element.points[1]))

    uf = UnionFind(len(endpoint_refs))
    for i, (_, _, pi) in enumerate(endpoint_refs):
        for j in range(i + 1, len(endpoint_refs)):
            if _dist(pi, endpoint_refs[j][2]) <= radius:
                uf.union(i, j)

    clusters: dict[int, list[int]] = {}
    for idx in range(len(endpoint_refs)):
        clusters.setdefault(uf.find(idx), []).append(idx)

    for members in clusters.values():
        if len(members) < 2:
            continue
        cx = sum(endpoint_refs[i][2][0] for i in members) / len(members)
        cy = sum(endpoint_refs[i][2][1] for i in members) / len(members)
        snapped = (round(cx, 1), round(cy, 1))
        for idx in members:
            element, point_index, _ = endpoint_refs[idx]
            pts = element.points[:]
            pts[point_index] = snapped
            element.points = pts


def _blob_geometry(blob: Element) -> tuple[float, float, float, float]:
    (x1, y1), (x2, y2) = blob.points[:2]
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    rx = abs(x2 - x1) / 2
    ry = abs(y2 - y1) / 2
    return cx, cy, max(rx, 1.0), max(ry, 1.0)


def _project_to_ellipse(
    center: tuple[float, float],
    radii: tuple[float, float],
    toward: tuple[float, float],
) -> tuple[float, float]:
    cx, cy = center
    rx, ry = radii
    dx = toward[0] - cx
    dy = toward[1] - cy
    denom = sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    if denom == 0:
        return center
    return (round(cx + dx / denom, 1), round(cy + dy / denom, 1))


def attach_to_blobs(elements: list[Element], margin: float) -> None:
    blobs = [element for element in elements if element.kind == "blob" and len(element.points) >= 2]
    for element in elements:
        if element.kind not in {"fermion", "gluon"} or len(element.points) < 2:
            continue
        pts = element.points[:]
        for point_index in (0, 1):
            point = pts[point_index]
            other = pts[1 - point_index]
            candidates: list[tuple[float, Element]] = []
            for blob in blobs:
                cx, cy, rx, ry = _blob_geometry(blob)
                dx = max(abs(point[0] - cx) - rx, 0)
                dy = max(abs(point[1] - cy) - ry, 0)
                gap = hypot(dx, dy)
                if gap <= margin:
                    candidates.append((gap, blob))
            if not candidates:
                continue
            _, blob = min(candidates, key=lambda item: item[0])
            cx, cy, rx, ry = _blob_geometry(blob)
            pts[point_index] = _project_to_ellipse((cx, cy), (rx, ry), other)
        element.points = pts


def fmt(value: float) -> str:
    if abs(value - round(value)) < 1e-6:
        return str(int(round(value)))
    return f"{value:.1f}"


def bounds(elements: list[Element], pad: float = 35.0) -> tuple[float, float, float, float]:
    pts: list[tuple[float, float]] = []
    for element in elements:
        pts.extend(element.points)
    min_x = min(p[0] for p in pts) - pad
    min_y = min(p[1] for p in pts) - pad
    max_x = max(p[0] for p in pts) + pad
    max_y = max(p[1] for p in pts) + pad
    return min_x, min_y, max_x, max_y


def tikz_source(xml_name: str, elements: list[Element], force_fermion_arrows: bool) -> str:
    min_x, min_y, max_x, max_y = bounds(elements)
    lines = [
        "\\documentclass[tikz,border=3pt]{standalone}",
        f"\\input{{{STYLE_FILE}}}",
        "",
        "\\begin{document}",
        "\\begin{tikzpicture}[fd diagram]",
        f"  \\path[use as bounding box] ({fmt(min_x)},{fmt(min_y)}) rectangle ({fmt(max_x)},{fmt(max_y)});",
        "",
        f"  % Generated from {xml_name} by jaxodraw_to_tikz.py.",
    ]
    last_kind = None
    for element in elements:
        if not element.points:
            continue
        if last_kind is not None and element.kind != last_kind:
            lines.append("")
        last_kind = element.kind
        if element.kind == "blob" and len(element.points) >= 2:
            (x1, y1), (x2, y2) = element.points[:2]
            lines.append(f"  \\fdblob{{{fmt(x1)}}}{{{fmt(y1)}}}{{{fmt(x2)}}}{{{fmt(y2)}}}")
        elif element.kind == "fermion" and len(element.points) >= 2:
            (x1, y1), (x2, y2) = element.points[:2]
            macro = "\\fdfermionarrow" if force_fermion_arrows or element.arrow else "\\fdfermion"
            lines.append(f"  {macro}{{{fmt(x1)}}}{{{fmt(y1)}}}{{{fmt(x2)}}}{{{fmt(y2)}}}")
        elif element.kind == "gluon" and len(element.points) >= 2:
            (x1, y1), (x2, y2) = element.points[:2]
            lines.append(f"  \\fdgluon{{{fmt(x1)}}}{{{fmt(y1)}}}{{{fmt(x2)}}}{{{fmt(y2)}}}")
        elif element.kind == "label":
            x, y = element.points[0]
            lines.append(f"  \\fdlabel{{{fmt(x)}}}{{{fmt(y)}}}{{{element.text}}}")
    lines.extend(["\\end{tikzpicture}", "\\end{document}", ""])
    return "\n".join(lines)


def report(elements: list[Element], radius: float) -> str:
    endpoint_refs: list[tuple[str, str, tuple[float, float]]] = []
    for element in elements:
        if element.kind in {"fermion", "gluon"} and len(element.points) >= 2:
            endpoint_refs.append((element.source_id, "start", element.points[0]))
            endpoint_refs.append((element.source_id, "end", element.points[1]))
    nearby: list[str] = []
    for i, (name_i, end_i, pi) in enumerate(endpoint_refs):
        close = []
        for j, (name_j, end_j, pj) in enumerate(endpoint_refs):
            if i == j:
                continue
            d = _dist(pi, pj)
            if d <= radius:
                close.append(f"{name_j}:{end_j}@({fmt(pj[0])},{fmt(pj[1])}) d={d:.1f}")
        if close:
            nearby.append(f"{name_i}:{end_i}@({fmt(pi[0])},{fmt(pi[1])}) -> " + "; ".join(close))
    return "\n".join(nearby)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snap-radius", type=float, default=8.0)
    parser.add_argument("--blob-margin", type=float, default=18.0)
    parser.add_argument("--no-force-fermion-arrows", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("sources", nargs="*", default=list(DEFAULT_SOURCES))
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    for source in args.sources:
        xml_path = base_dir / source
        elements = parse_jaxodraw(xml_path)
        if args.report:
            print(f"\n## {source}")
            print(report(elements, args.snap_radius))
        attach_to_blobs(elements, args.blob_margin)
        snap_vertices(elements, args.snap_radius)
        output = xml_path.with_name(f"{xml_path.stem}-tikz.tex")
        output.write_text(
            tikz_source(source, elements, not args.no_force_fermion_arrows),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
