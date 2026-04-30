#!/usr/bin/env python3
"""Lightweight structural and layout checks for draw.io XML.

This is intentionally dependency-free. It catches common issues that make first
renders ugly: clipped shapes, duplicate IDs, missing geometry, labeled edges,
and overlapping non-container vertices.
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Vertex:
    id: str
    value: str
    style: str
    x: float
    y: float
    w: float
    h: float

    @property
    def area(self) -> float:
        return max(0.0, self.w) * max(0.0, self.h)

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    @property
    def is_container(self) -> bool:
        s = self.style.lower()
        if "swimlane" in s:
            return True
        if "verticalalign=top" in s and self.w >= 160 and self.h >= 90:
            return True
        if self.value.lower() in {"aws cloud", "vpc"}:
            return True
        return False

    @property
    def is_text_only(self) -> bool:
        s = self.style.lower()
        return s.startswith("text;") or "strokeColor=none".lower() in s.lower()


def num(value: str | None, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def intersection(a: Vertex, b: Vertex) -> float:
    x1 = max(a.x, b.x)
    y1 = max(a.y, b.y)
    x2 = min(a.right, b.right)
    y2 = min(a.bottom, b.bottom)
    if x2 <= x1 or y2 <= y1:
        return 0.0
    return (x2 - x1) * (y2 - y1)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <diagram.drawio>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    errors: list[str] = []
    warnings: list[str] = []

    if "<!--" in text or "-->" in text:
        errors.append("XML comments are forbidden in generated draw.io files")

    try:
        tree = ET.ElementTree(ET.fromstring(text))
    except ET.ParseError as exc:
        print(f"ERROR: XML parse failed: {exc}")
        return 1

    root = tree.getroot()
    page_w = num(root.attrib.get("pageWidth"), 850)
    page_h = num(root.attrib.get("pageHeight"), 1100)

    cells = root.findall(".//mxCell")
    ids: dict[str, int] = {}
    vertices: list[Vertex] = []

    for cell in cells:
        cid = cell.attrib.get("id", "")
        if cid:
            ids[cid] = ids.get(cid, 0) + 1

        geom = cell.find("mxGeometry")
        if cell.attrib.get("vertex") == "1":
            if geom is None:
                errors.append(f"vertex {cid!r} has no mxGeometry")
                continue
            v = Vertex(
                id=cid,
                value=re.sub(r"<[^>]+>", "", cell.attrib.get("value", "")).replace("&#xa;", " "),
                style=cell.attrib.get("style", ""),
                x=num(geom.attrib.get("x")),
                y=num(geom.attrib.get("y")),
                w=num(geom.attrib.get("width")),
                h=num(geom.attrib.get("height")),
            )
            vertices.append(v)
            if v.w <= 0 or v.h <= 0:
                errors.append(f"vertex {cid!r} has non-positive dimensions")
            if v.x < 0 or v.y < 0 or v.right > page_w or v.bottom > page_h:
                errors.append(
                    f"vertex {cid!r} is outside page bounds: "
                    f"({v.x:g},{v.y:g},{v.w:g},{v.h:g}) page=({page_w:g},{page_h:g})"
                )

        if cell.attrib.get("edge") == "1":
            if geom is None:
                errors.append(f"edge {cid!r} has no mxGeometry")
            elif geom.attrib.get("relative") != "1":
                warnings.append(f"edge {cid!r} geometry should usually have relative=1")
            if cell.attrib.get("value", "").strip():
                warnings.append(f"edge {cid!r} has an inline label; prefer separate text labels to avoid collisions")

    dupes = sorted(k for k, count in ids.items() if count > 1)
    for cid in dupes:
        errors.append(f"duplicate mxCell id: {cid!r}")

    if "0" not in ids or "1" not in ids:
        errors.append('required root cells id="0" and id="1" are missing')

    noncontainers = [v for v in vertices if not v.is_container and not v.is_text_only]
    for i, a in enumerate(noncontainers):
        for b in noncontainers[i + 1 :]:
            overlap = intersection(a, b)
            if overlap <= 0:
                continue
            ratio = overlap / max(1.0, min(a.area, b.area))
            if ratio >= 0.10:
                warnings.append(f"vertices {a.id!r} and {b.id!r} overlap by {ratio:.0%} of the smaller area")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")

    if errors:
        return 1
    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
