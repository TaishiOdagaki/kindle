# Japanese Culture Press

Independent, self-published Kindle books about Japanese pop culture, written for an international fan audience. Not affiliated with, endorsed by, or representing any academic institution, publisher, or rights holder discussed within any title — see each book's own front-matter disclaimer for specifics.

"Japanese Culture Press" is a publishing label/imprint for this project, not a claim of institutional, nonprofit, or academic status. (An earlier direction considered naming it as a formal "society," but that was dropped — it sat too close to real organizations with similar names, like the Pittsburgh Japanese Culture Society or the various city-level Japan Societies, and risked implying an institutional affiliation this project doesn't have.)

## Books in this series

| Book | Folder | Status | Author byline |
|---|---|---|---|
| *The Japan They Never Told You* | [`book/`](book/) | Draft manuscript | (none yet — unsigned) |
| *Chainsaw Man: The Devil in the Details* | [`chainsaw-man-book/`](chainsaw-man-book/) | **Published** | Jiro Naozane (pen name) |
| *Demon Slayer: Total Concentration* | [`demon-slayer-book/`](demon-slayer-book/) | Draft manuscript, cover pending | Jiro Naozane (pen name) |

Each book folder has its own `README.md` with publishing notes, KDP conversion instructions, and a pre-publish checklist specific to that title.

## Conventions for future books in this series

- **One folder per book**, with its own `manuscript.md` and `README.md`.
- **"A Japanese Culture Press Book"** on the title page, under the title/subtitle.
- **Author bylines** are pen names with generic, non-verifiable backgrounds (e.g., "studied Japanese culture at university") — never a named real institution, real research group, or specific professional credential that isn't true. See the `chainsaw-man-book/` project history for why: two earlier naming attempts (a fictional academic society, a specific real university club) both turned out to collide with real organizations and got dropped for that reason.
- **Trademark/rights disclaimers** in the front matter of any book discussing a specific copyrighted work, naming the relevant rights holders as unaffiliated.
- **No reproduced copyrighted art, panels, or extended text** from any work discussed — commentary and original analysis only.
- **AI-generated content disclosure**: both manuscript text and any AI-generated cover art need to be disclosed in KDP's content-origin declaration at publishing time, regardless of how much subsequent editing/art-direction happened. This is a KDP compliance step for each book, not a one-time setup.
- **Book descriptions are delivered paste-ready**: any KDP product-page description gets written directly in KDP-supported HTML (`<p>`, `<b>`, `<i>`, etc.) as its own `kdp-book-description.txt` in the book's folder, not as plain text needing reformatting later. Keep the total length, HTML markup included, under KDP's 4,000-character limit — the limit counts the tags, not just the visible text.
- **Every manuscript gets a `verify-nonfiction-claims` audit pass before publishing**, not just a read-through. The *Chainsaw Man* book shipped, and only afterward turned out to have several confident, fluently-written factual errors (a spliced/misattributed quote, a whole chapter built on a wrong claim about which magazine serialized the manga, a citation to interviews that didn't exist, a backwards etymology claim) — all found only because the user happened to ask. Run the audit *before* that happens, not after.
