# The Builder’s Terminal

Original profile artwork inspired by the portfolio’s visual identity: graphite #101412, lime #A3E635, warm white #F4F2E9; construction lines, chapter markers and terminal typography. Slogan: “Behind every line of code, there is a builder.”

Banner and ASCII/info panel are self-contained animated SVGs. Motion is short, runs once and respects reduced motion where the image renderer supports it. Static counterparts remain available in `assets/`. Core professional information and project descriptions are also real Markdown, not image-only text. No scripts or remote font dependencies are embedded in images.

The portrait is a deterministic ASCII conversion of Isaac’s approved photograph. It is cropped to the face/shoulders, with lime background suppressed. No source photo is published.

Local regeneration (Python with Pillow):

    python scripts/fetch_contributions.py
    python scripts/build_profile.py /path/to/approved-photo.png

Calendar-only regeneration uses Python’s standard library, no dependencies or personal access token:

    python scripts/fetch_contributions.py
    python scripts/build_profile.py --heatmap-only

The public GitHub contribution fragment is parsed and validated for dates, counts, levels and contiguous coverage. Unknown upstream markup causes failure before replacing stored data. The workflow stops on failure, preserving the last committed assets. Its schedule is approximate; GitHub can delay or disable inactive scheduled workflows. Only the calendar job has repository contents-write permissions; official actions are pinned to commit SHAs. No push trigger or external widget service is used.

Public contribution counts can include anonymized private activity if the account owner has enabled it on GitHub. No private repository names, files or code are fetched. Activity is not presented as a skill score.

The main README is English, with a Portuguese presentation and full stack in expandable sections. Cards are vertically arranged to remain readable on small screens. Private projects link only to authorized portfolio summaries.
