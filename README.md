# pi-drawio

A Pi package that adds a `drawio` skill for generating native draw.io diagrams as `.drawio` files and optionally exporting them to PNG, SVG, PDF, or JPG.

PNG, SVG, and PDF exports use draw.io Desktop's CLI with embedded diagram XML, so exported files remain editable in draw.io.

## Install

Recommended: install as a Pi package from GitHub:

```bash
pi install git:github.com/ethanolivertroy/pi-drawio
```

Then restart Pi or run `/reload` in an existing Pi session.

For a project-local install, add `-l` from the project directory:

```bash
pi install -l git:github.com/ethanolivertroy/pi-drawio
```

To try it for one run without adding it to settings:

```bash
pi -e git:github.com/ethanolivertroy/pi-drawio
```

After install, use the skill command:

```text
/skill:drawio create a flowchart for password reset
/skill:drawio png architecture diagram for a web app with CDN, API, queue, workers, and Postgres
/skill:drawio svg ER diagram for users, teams, projects, and tasks
```

You can also ask naturally; Pi should load the skill when your request mentions diagrams, draw.io, `.drawio`, PNG/SVG/PDF export, architecture diagrams, ER diagrams, flowcharts, mockups, and related tasks.

### Manual clone alternative

If you prefer not to use `pi install`, clone into a skill discovery directory:

```bash
git clone https://github.com/ethanolivertroy/pi-drawio ~/.pi/agent/skills/pi-drawio
```

Pi recursively discovers `skills/drawio/SKILL.md` from that checkout.

## What it does

- Generates native draw.io `mxGraphModel` XML.
- Writes `.drawio` files directly; no server-side conversion required.
- Optionally exports with draw.io Desktop CLI.
- Embeds diagram XML into PNG, SVG, and PDF exports.
- Opens the result when possible.
- Includes layout quality guidance to reduce clipping, label collisions, and messy edge routing.
- Includes helper scripts for layout checks, export, opening, and optional post-processing.

## Optional requirements

Exporting requires draw.io Desktop to be installed. The skill still works without it by producing `.drawio` files you can open manually.

CLI locations checked by the helper:

- `drawio` or `draw.io` on `PATH`
- macOS: `/Applications/draw.io.app/Contents/MacOS/draw.io`
- WSL2 default and per-user Windows install paths

## Package structure

```text
package.json                       Pi package manifest
skills/drawio/SKILL.md             Skill instructions
skills/drawio/scripts/             Export/open/check helpers
skills/drawio/references/          XML and layout references
```

## Update or remove

```bash
pi update git:github.com/ethanolivertroy/pi-drawio
pi remove git:github.com/ethanolivertroy/pi-drawio
```

## License

MIT
