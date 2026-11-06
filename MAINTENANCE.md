# Profile maintenance

`python3 scripts/generate.py` fetches public GitHub data and renders both SVG sizes using Python's standard library. `python3 scripts/generate.py --offline` rebuilds from the committed snapshot. No third-party statistics service, font download, JavaScript, animation or foreignObject is required to display the profile.

The ASCII globe is generated mathematically. Desktop uses a two-column terminal; `<picture>` selects the single-column asset below 600px. Both use an opaque near-black background, so their contrast is independent of the GitHub theme. Content is also available as native Markdown, including clickable project/contact links and a text alternative.

The workflow runs daily at 09:23 UTC (06:23 São Paulo), manually, and on generator/workflow changes. It uses only the repository's GITHUB_TOKEN, with contents:write to commit assets. No personal token is needed. Failed fetches stop generation and preserve the last snapshot. GitHub can delay scheduled jobs and disable them after 60 days without repository activity; use Actions → Update terminal profile → Run workflow to refresh manually.

## Evidence

Stack and project descriptions were checked against public READMEs and manifests in connections-hub, tasks, wsn-front and chamados-repo. Archived status is explicitly stated. Linux is user-provided context; Windows is also the documented target of Tasks. No private repository content is published. Python is used to maintain this profile, not presented as prior professional experience.

## Official references

- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
- https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
- https://docs.github.com/en/actions/tutorials/authenticate-with-github_token
