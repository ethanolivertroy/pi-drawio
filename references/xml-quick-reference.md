# Draw.io XML Quick Reference

Use this reference when generating native `.drawio` files.

## Minimal file

```xml
<mxGraphModel adaptiveColors="auto" dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
  </root>
</mxGraphModel>
```

## Rounded rectangle vertex

```xml
<mxCell id="step-1" value="Start" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="80" y="80" width="140" height="60" as="geometry"/>
</mxCell>
```

## Decision diamond

```xml
<mxCell id="decision-1" value="Valid?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
  <mxGeometry x="280" y="70" width="120" height="80" as="geometry"/>
</mxCell>
```

## Cylinder / database

```xml
<mxCell id="db-1" value="Database" style="shape=cylinder3d;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
  <mxGeometry x="480" y="70" width="120" height="80" as="geometry"/>
</mxCell>
```

## Actor / user

```xml
<mxCell id="actor-1" value="User" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;" vertex="1" parent="1">
  <mxGeometry x="40" y="80" width="30" height="60" as="geometry"/>
</mxCell>
```

## Container / swimlane

```xml
<mxCell id="lane-1" value="Frontend" style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="720" height="180" as="geometry"/>
</mxCell>
```

Child cells can use `parent="lane-1"` with coordinates relative to the container.

## Edge

```xml
<mxCell id="edge-1" value="" style="endArrow=block;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1" source="step-1" target="decision-1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Edge with label

```xml
<mxCell id="edge-yes" value="yes" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="decision-1" target="step-2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Orthogonal edge with waypoints

```xml
<mxCell id="edge-2" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="220" y="160"/>
      <mxPoint x="340" y="160"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## Common fill/stroke colors

- Blue: `fillColor=#dae8fc;strokeColor=#6c8ebf;`
- Green: `fillColor=#d5e8d4;strokeColor=#82b366;`
- Yellow: `fillColor=#fff2cc;strokeColor=#d6b656;`
- Red: `fillColor=#f8cecc;strokeColor=#b85450;`
- Purple: `fillColor=#e1d5e7;strokeColor=#9673a6;`
- Gray: `fillColor=#f5f5f5;strokeColor=#666666;`

## Well-formedness checklist

- No XML comments.
- Escape `&`, `<`, `>`, and quotes in attribute values.
- Unique IDs.
- Root cells `0` and `1` exist.
- Vertices have geometry with dimensions.
- Edges have non-self-closing geometry.
