---
name: drawio
description: Always use when the user asks to create, generate, draw, or design a diagram, flowchart, architecture diagram, ER diagram, sequence diagram, class diagram, network diagram, mockup, wireframe, UI sketch, draw.io/drawio/drawoi, .drawio files, or diagram export to PNG/SVG/PDF/JPG.
license: MIT
compatibility: Pi or any Agent Skills-compatible coding agent with file write and shell access. Optional export requires draw.io Desktop CLI.
---

# Draw.io Diagram Skill

Generate native draw.io diagrams as `.drawio` files. When requested, export them to PNG, SVG, or PDF with embedded diagram XML so the exported file remains editable in draw.io.

## Workflow

1. Determine the requested diagram type, filename, and output format.
2. Generate draw.io XML directly in `mxGraphModel` format.
3. Write the XML to a `.drawio` file in the current working directory.
4. Validate XML well-formedness and run the lightweight layout checker when possible.
5. Apply the visual quality rules in `references/layout-quality.md`: margins, spacing, explicit edge routing, no clipped actors, and no edge-label collisions.
6. Optionally post-process edge routing if the helper can run without installing anything.
7. If the user requested PNG/SVG/PDF/JPG, export with the draw.io Desktop CLI if available.
8. For image exports, visually self-review the rendered PNG/SVG/PDF when the environment allows reading or previewing it.
9. Open the exported result, or the `.drawio` source if no export was requested or export is unavailable.
10. If opening fails, print the absolute file path.

Use the scripts in this skill directory when helpful:

```bash
./scripts/check-drawio-layout.py diagram.drawio
./scripts/postprocess-drawio.sh diagram.drawio
./scripts/drawio-export.sh diagram.drawio png diagram.drawio.png
./scripts/open-result.sh diagram.drawio.png
```

When using scripts from another directory, call them with their full path, for example:

```bash
/Users/ethantroy/.agents/skills/drawio/scripts/drawio-export.sh diagram.drawio svg diagram.drawio.svg
```

## Choosing the output format

Infer the output format from the user's request.

Examples:

- `/drawio create a flowchart` -> `flowchart.drawio`
- `/drawio png flowchart for login` -> `login-flow.drawio.png`
- `/drawio svg: ER diagram` -> `er-diagram.drawio.svg`
- `/drawio pdf architecture overview` -> `architecture-overview.drawio.pdf`
- `/drawio jpg homepage wireframe` -> `homepage-wireframe.drawio.jpg`

If no format is mentioned, create and open only the `.drawio` file.

### Supported export formats

| Format | Embed XML | Notes |
|--------|-----------|-------|
| `png` | Yes (`-e`) | Viewable everywhere, editable in draw.io |
| `svg` | Yes (`-e`) | Scalable, editable in draw.io |
| `pdf` | Yes (`-e`) | Printable, editable in draw.io |
| `jpg` | No | Lossy; no embedded XML support |

Use double extensions for exports: `name.drawio.png`, `name.drawio.svg`, `name.drawio.pdf`, or `name.drawio.jpg`.

After a successful PNG/SVG/PDF export, delete the intermediate `.drawio` file because the exported file embeds the diagram XML. Do not delete the `.drawio` file for JPG exports because JPG cannot embed editable diagram XML.

## File naming

- Use a descriptive filename based on the content.
- Use lowercase words separated by hyphens.
- Avoid spaces and punctuation.
- Preserve `.drawio` before the export extension.

Examples: `login-flow.drawio`, `database-schema.drawio.svg`, `network-topology.drawio.pdf`.

## XML format

A `.drawio` file is native mxGraphModel XML. Always generate XML directly. Do not save Mermaid, PlantUML, CSV, or pseudo-code when the user requested draw.io.

Every diagram must include the required root cells:

```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
  </root>
</mxGraphModel>
```

All normal diagram elements use `parent="1"` unless intentionally creating layers or containers.

### Required edge structure

Edges must not be self-closing. Every edge needs a geometry child:

```xml
<mxCell id="edge-1" value="" edge="1" parent="1" source="source-id" target="target-id" style="endArrow=block;html=1;rounded=0;">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Visual layout quality rules

Good XML is not enough. The diagram must render cleanly.

Mandatory layout rules:

- Keep visible elements at least 40 px inside the page bounds.
- Never place actors, labels, or arrowheads partly off-canvas.
- Keep nodes away from container borders and swimlane headers.
- Use a grid with generous row/column spacing.
- Avoid edge labels by default; labels on edges often collide with nodes after draw.io routing.
- Prefer descriptive node text or separate text cells placed away from connectors.
- Use explicit orthogonal edge routing with `exitX`, `exitY`, `entryX`, `entryY`, and waypoints for non-trivial edges.
- Avoid arrows crossing through node text, other nodes, or container labels.
- For cloud architecture diagrams, put edge services on the top row, network/VPC in the middle, app/data tiers inside subnets, and regional managed services clearly inside the cloud boundary.
- After export, visually self-review the rendered image if possible and fix clipped content, label collisions, crossing arrows, or confusing containment before final response.

Run the bundled checker when possible:

```bash
/path/to/drawio/scripts/check-drawio-layout.py diagram.drawio
```

Then consult `references/layout-quality.md` for detailed rules and patterns.

## XML well-formedness rules

These rules are mandatory:

- Never include XML comments (`<!-- ... -->`) in generated diagram XML.
- Escape attribute values: `&amp;`, `&lt;`, `&gt;`, `&quot;`.
- Use unique `id` values for all `mxCell` elements.
- Include `id="0"` and `id="1"` root cells.
- Give every vertex an `mxGeometry` child with `x`, `y`, `width`, `height`, and `as="geometry"`.
- Give every edge an `mxGeometry relative="1" as="geometry"` child.
- Prefer simple, valid styles over overly clever styles.
- Avoid double hyphens anywhere in XML text, especially if user-provided labels might later be copied into comments by tools.

Useful validation commands:

```bash
python3 - <<'PY'
import sys, xml.etree.ElementTree as ET
ET.parse(sys.argv[1])
print('XML OK')
PY diagram.drawio
```

## Draw.io CLI export

The draw.io Desktop app includes a command-line export interface. Prefer the bundled helper script because it handles macOS, Linux, and WSL2 detection:

```bash
/path/to/drawio/scripts/drawio-export.sh <input.drawio> <png|svg|pdf|jpg> [output-file]
```

The helper uses:

```bash
drawio -x -f <format> -e -b 10 -o <output> <input.drawio>
```

For JPG, the helper omits `-e` because editable XML cannot be embedded in JPG.

If the CLI is not found, keep the `.drawio` file and tell the user they can install draw.io Desktop to enable export, or open the `.drawio` file directly.

### CLI locations checked

- `drawio` on `PATH`
- `draw.io` on `PATH`
- macOS: `/Applications/draw.io.app/Contents/MacOS/draw.io`
- WSL2 default: `/mnt/c/Program Files/draw.io/draw.io.exe`
- WSL2 per-user: `/mnt/c/Users/<WindowsUser>/AppData/Local/Programs/draw.io/draw.io.exe`
- Linux native: `drawio` on `PATH`

## Optional edge-routing post-processing

If available locally, `npx --no-install @drawio/postprocess` can optimize edge routing. Use the helper and skip failures silently:

```bash
/path/to/drawio/scripts/postprocess-drawio.sh diagram.drawio
```

Do not install `@drawio/postprocess` automatically. Do not ask the user about it.

## Opening the result

Use the helper when possible:

```bash
/path/to/drawio/scripts/open-result.sh <file>
```

Equivalent platform commands:

| Environment | Command |
|-------------|---------|
| macOS | `open <file>` |
| Linux | `xdg-open <file>` |
| WSL2 | `cmd.exe /c start "" "$(wslpath -w <file>)"` |
| Windows shell | `start <file>` |

## Reference

For more draw.io XML patterns, consult `references/xml-quick-reference.md` in this skill. For layout rules and visual quality checks, consult `references/layout-quality.md`. For the complete upstream reference, fetch and follow:

https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/xml-reference.md

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| CLI not found | draw.io Desktop is not installed or not on `PATH` | Keep/open the `.drawio` file and mention draw.io Desktop for export |
| Export is empty or corrupt | Invalid XML or missing geometry | Validate XML and fix mxGraphModel structure |
| Diagram opens blank | Missing root cells or elements placed off canvas | Ensure `id="0"`, `id="1"`, sane coordinates, and visible styles |
| Edges do not render | Edge is self-closing or missing source/target | Add edge geometry child and valid source/target IDs |
| Exported file not editable | Export omitted `-e`, or format is JPG | Use PNG/SVG/PDF with embedded diagram XML |
