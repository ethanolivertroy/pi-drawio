# Draw.io Skill for Pi

An Agent Skills-compatible skill for generating native draw.io diagrams as `.drawio` files and optionally exporting them to PNG, SVG, PDF, or JPG.

The PNG, SVG, and PDF export path uses draw.io Desktop's CLI with embedded diagram XML, so exported files remain editable in draw.io.

## Install

Clone this repository into a Pi skill discovery directory:

```bash
git clone https://github.com/ethanolivertroy/drawio-skill ~/.agents/skills/drawio
```

Restart Pi, then ask for diagrams naturally:

```text
/drawio create a flowchart for password reset
/drawio png architecture diagram for a web app with CDN, API, queue, workers, and Postgres
/drawio svg ER diagram for users, teams, projects, and tasks
```

You can also load it explicitly:

```bash
pi --skill ~/.agents/skills/drawio
```

## What it does

- Generates native draw.io `mxGraphModel` XML.
- Writes `.drawio` files directly; no server-side conversion required.
- Optionally exports with draw.io Desktop CLI.
- Embeds diagram XML into PNG, SVG, and PDF exports.
- Opens the result when possible.
- Includes helper scripts for export, opening, and optional post-processing.

## Optional requirements

Exporting requires draw.io Desktop to be installed. The skill still works without it by producing `.drawio` files you can open manually.

CLI locations checked by the helper:

- `drawio` or `draw.io` on `PATH`
- macOS: `/Applications/draw.io.app/Contents/MacOS/draw.io`
- WSL2 default and per-user Windows install paths

## Files

```text
SKILL.md                         Skill instructions
scripts/drawio-export.sh          Export helper
scripts/open-result.sh            Cross-platform open helper
scripts/postprocess-drawio.sh     Optional no-install postprocess helper
references/xml-quick-reference.md XML snippets and rules
```

## License

MIT
