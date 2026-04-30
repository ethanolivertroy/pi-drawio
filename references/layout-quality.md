# Draw.io Layout Quality Guide

Use this guide before opening or exporting a diagram. The goal is a diagram that looks clean on first render, not just XML that parses.

## Required visual quality checks

- Keep every visible element at least 40 px inside the page bounds.
- Keep external actors fully visible; never place them partly outside the page.
- Use generous spacing: at least 40 px between peer nodes and 60 px between major rows.
- Do not place service nodes on top of container borders or swimlane headers.
- Put nodes fully inside the container they conceptually belong to.
- Avoid edge labels by default. Edge labels often render over nodes or lines.
- Prefer self-explanatory node text over edge labels, for example `ALB HTTPS listener` instead of an edge label `HTTPS`.
- Use explicit orthogonal routing for edges that are not simple adjacent left-to-right or top-to-bottom connections.
- Avoid edges through nodes, swimlane headers, or container borders when a waypoint can route around them.
- Avoid long diagonal lines. Use orthogonal edges with waypoints.
- Keep arrows from crossing text.
- Export to PNG/SVG when possible and visually inspect the rendered result before finalizing.

## Layout pattern for cloud architecture diagrams

Use a predictable grid:

1. Title at top with no connectors near it.
2. External users/systems on the far left with enough margin.
3. Edge/network services on the top row inside the cloud boundary.
4. VPC boundary in the middle.
5. Public subnets above private subnets inside the VPC.
6. Application services centered in private subnets.
7. Datastores either in a dedicated data subnet or clearly inside the VPC.
8. Regional managed services such as CloudWatch, Secrets Manager, S3, and Route 53 inside the cloud boundary but outside the VPC unless the architecture says otherwise.

## Edge routing rules

For adjacent nodes in one row, use horizontal side anchors:

```xml
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
```

For vertical parent-to-child flow, use top/bottom anchors:

```xml
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
```

For long or branching routes, add waypoints:

```xml
<mxGeometry relative="1" as="geometry">
  <Array as="points">
    <mxPoint x="640" y="460"/>
    <mxPoint x="440" y="460"/>
  </Array>
</mxGeometry>
```

## Safer labels

Prefer separate text cells near an edge instead of edge `value` labels when labels are necessary:

```xml
<mxCell id="label-https" value="HTTPS" style="text;html=1;strokeColor=none;fillColor=#ffffff;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=11;" vertex="1" parent="1">
  <mxGeometry x="330" y="175" width="50" height="20" as="geometry"/>
</mxCell>
```

Place text labels where they do not overlap nodes, arrowheads, or container borders.

## Final self-review checklist

Before answering the user, ask:

- Is anything clipped at the page edge?
- Do any labels collide with nodes, arrows, or borders?
- Do arrows run through node text?
- Are containers behind their children rather than on top?
- Are all important services visibly inside the right boundary?
- Would the diagram still be readable when scaled down in a screenshot?
