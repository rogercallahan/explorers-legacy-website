"""Build the reviewed, screen-light ELS expedition catalog using only the stdlib."""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ('Science', 'Technology', 'Engineering', 'Arts', 'Mathematics')
SOURCES = {
    'nasa': ('NASA Space Place', 'https://spaceplace.nasa.gov/', 'Further exploration of space, Earth and observation.'),
    'exploratorium': ('Exploratorium Science Snacks', 'https://www.exploratorium.edu/snacks', 'Further hands-on exploration of physical and natural phenomena.'),
    'cs': ('CS Unplugged', 'https://www.csunplugged.org/en/', 'Further exploration of computing concepts without a computer.'),
    'engineering': ('TeachEngineering: Engineering Design Process', 'https://www.teachengineering.org/popular-topics/engineering-design-process', 'Background on iterative design, criteria, constraints and testing.'),
    'art': ('National Gallery of Art: Educational Resources', 'https://www.nga.gov/educational-resources', 'Further exploration of looking, making and interpreting art.'),
    'math': ('University of Cambridge NRICH', 'https://nrich.maths.org/', 'Further mathematical investigations and problem solving.'),
    'signals': ('ELS Signals in the Sky field notes', '../signals-in-the-sky.html', 'The existing ELS aviation expedition and its credited sources.'),
}
PREFIXES = dict(zip(CATEGORIES, ('SCI', 'TEC', 'ENG', 'ART', 'MAT')))
ESC = html.escape

def catalog():
    items = []
    for category in CATEGORIES:
        rows = (ROOT / 'content' / (category.lower() + '.txt')).read_text(encoding='utf-8').splitlines()
        for n, row in enumerate(filter(None, rows), 1):
            fields = row.split('|')
            if len(fields) != 9:
                raise ValueError(f'{category} row {n}: expected 9 fields, got {len(fields)}')
            title, question, materials, steps, evidence, explanation, extension, safety, source = fields
            instructions = steps.split(' / ')
            if len(instructions) != 3 or source not in SOURCES:
                raise ValueError(f'Invalid steps or reference: {title}')
            duration = {'Moon Journal': 'Five evenings; about 10 minutes each', 'Seed Water Watch': 'Five days; about 10 minutes each', 'Evaporation Marks': 'Several days; about 5 minutes each', 'Soil Settling': 'Two days; three brief observations', 'Habitat From a Window': 'Three 10-minute observations', 'Shadow Detectives': 'Three brief observations across one day'}.get(title, 'About 20–40 minutes; pause whenever useful')
            items.append(dict(id=f'{PREFIXES[category]}-{n:03}', category=category, title=title,
                question=question, materials=materials, steps=instructions, evidence=evidence,
                explanation=explanation, extension=extension, safety=safety, source=source,
                duration=duration, mode='Family activity; adapt together',
                status='authored; not field-tested', added='2026-11-09',
                existing_lesson='../signals-in-the-sky.html' if source == 'signals' else None))
        if n != 25:
            raise ValueError(f'{category}: expected 25 expeditions, got {n}')
    return items

def header(title):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ESC(title)} | Explorers Legacy Studios</title><link rel="stylesheet" href="../assets/learn.css"><link rel="stylesheet" href="../assets/expeditions.css">
</head><body><a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header"><a class="brand" href="../index.html" aria-label="Explorers Legacy Studios Home"><span class="compass-mark"><img src="../assets/images/explorer_compass_circle.png" alt="" width="54" height="54"></span><span class="brand-copy"><span class="brand-name">EXPLORERS LEGACY</span><span class="brand-subtitle">STUDIOS</span></span></a><nav aria-label="Main navigation"><a href="../index.html">Home</a><a href="../learn.html">Learn</a><a href="../about.html">About</a></nav></header>
<main id="main-content" tabindex="-1">'''

def footer():
    return '''</main><footer><a href="../learn.html#expedition-library">Back to Learn expeditions</a><p>Onward to Discovery.</p></footer><script src="../assets/expeditions.js" defer></script></body></html>'''

def expedition(item):
    e = {k: ESC(v) if isinstance(v, str) else v for k, v in item.items()}
    source_title, url, purpose = SOURCES[item['source']]
    source = f'<a href="{ESC(url)}">{ESC(source_title)}</a>'
    link = '<p><a href="../signals-in-the-sky.html">Open the original Signals in the Sky expedition</a></p>' if item['existing_lesson'] else ''
    steps = ''.join('<li>' + ESC(step) + '</li>' for step in item['steps'])
    return f'''<details class="expedition" id="{e['id']}" data-title="{e['title'].lower()}">
<summary><span class="expedition-id">{e['id']}</span><span class="expedition-title">{e['title']}</span></summary>
<div class="expedition-body"><p class="expedition-meta">{e['mode']} · {e['duration']}</p>
<h2>Begin with a question</h2><p class="lede">{e['question']}</p>{link}
<h3>Gather</h3><p>{e['materials']}.</p>
<p class="safety"><strong>Before you begin:</strong> {e['safety']}</p>
<h3>Predict, explore, revise</h3><ol>{steps}</ol>
<h3>Keep your evidence</h3><p>{e['evidence']}</p>
<h3>Make sense of it</h3><p>{e['explanation']}</p>
<h3>Keep wondering</h3><p>{e['extension']}</p>
<p><strong>Share your reasoning:</strong> Explain what you observed, what you think it means, and one thing this activity cannot establish. A surprising result or an honest “I don’t know yet” is useful evidence.</p>
<p class="adaptation"><strong>Make it work for you:</strong> Sketch, dictate to a trusted adult, or describe your evidence instead of writing. A partner can handle materials or measurements. If a step is inaccessible, discuss its prediction and clearly label it untested.</p>
<h3>Explore a reference</h3><p>{source} — {ESC(purpose)}</p><p class="reference-note">Original ELS activity. This reference offers background or further learning; it does not certify this activity or establish its learning effectiveness. External sites have their own privacy practices; an adult can open the reference or select a printed alternative.</p>
<div class="journal"><h3>Explorer’s paper journal</h3><p>Prediction: ________________________________________</p><p>Observation / measurement: __________________________</p><p>My explanation and its limits: ________________________</p><p>What I would try next: _______________________________</p></div>
<div class="expedition-actions"><a href="#{e['id']}">Link to {e['id']}</a><button type="button" class="print-expedition" data-expedition="{e['id']}" hidden>Print this expedition</button><a href="#catalog-top">Back to expedition list</a></div>
</div></details>'''

def build():
    items = catalog()
    outputs = {}
    outputs['assets/expeditions/catalog.json'] = json.dumps({'schema_version': 1, 'catalog_version': '2026-11-09', 'sources': {k: dict(title=v[0], url=v[1], purpose=v[2]) for k,v in SOURCES.items()}, 'expeditions': items}, ensure_ascii=False, indent=2) + '\n'
    for category in CATEGORIES:
        subset = [i for i in items if i['category'] == category]
        title = category + ' Expeditions'
        links = ''.join(f'<a href="{c.lower()}.html"'+ (' aria-current="page"' if c == category else '') + f'>{c} · 25</a>' for c in CATEGORIES)
        index = ''.join(f'<li><a href="#{e["id"]}">{e["id"]} — {ESC(e["title"])}</a></li>' for e in subset)
        body = f'''<p class="eyebrow">The Explorer’s Institute · Learn</p><h1>{title}</h1><p class="lede">25 ways to ask, observe, create and explain. Choose what interests you; there is no streak or required order.</p>
<nav class="section-links" aria-label="STEAM expeditions">{links}</nav>
<section class="family-note" aria-label="Family guide"><h2>Start together, then explore</h2><p>Read the materials and safety note with a trusted adult. These are starting activities for family use, not tested age certifications or claims of guaranteed learning. Adults choose suitable materials, supervision and locations. Use blunt scissors only with adult help. Keep small parts away from young children and pets.</p><p>Keep observations in your own notebook. This catalog does not ask for an account, collect journal entries, award points or use AI to judge your work. You can print instructions and step away from the screen. Outdoor activities can become window observations when conditions or access make that better.</p></section>
<section id="catalog-top"><h2>Choose an expedition</h2><div class="expedition-search" hidden><label for="expedition-search">Find a title or expedition ID</label><input id="expedition-search" type="search" placeholder="Search these 25 expeditions"><p id="expedition-count" role="status">25 expeditions</p><button type="button" id="clear-search">Show all expeditions</button></div><ol class="expedition-index">{index}</ol></section>
<section aria-label="Expedition instructions">{''.join(expedition(i) for i in subset)}</section>'''
        outputs['expeditions/' + category.lower() + '.html'] = header(title) + body + footer()
    review = ['# ELS STEAM expedition batch — 9 November 2026', '', '## Scope and counting', '', '125 catalog expeditions: 25 each in Science, Technology, Engineering, Arts and Mathematics. TEC-001 extends and links the existing Signals in the Sky lesson; it is not counted a second time. The other 124 entries are new original ELS activities. Existing Learn articles remain separate from expedition counts.', '', 'This is website content and reusable JSON, not a native Android screen rollout. No additional third-party accounts, analytics, AI calls, uploads or child-data storage are introduced.', '', '## Editorial status', '', 'All activities are authored starting versions for family use. They have not been field-tested with children, independently safety-certified or validated for learning outcomes. The brief duration estimates are planning aids. Each activity supplies a question, materials, three actionable steps, an evidence product, explanation, extension, specific safety note and optional reference. Activities remain usable without opening external references, except that Signals links its existing ELS companion lesson.', '', 'Background links are further-learning resources, not claims that a provider authored, endorsed or evaluated the ELS text. No third-party lesson text or imagery is copied. The existing branding is retained. Family feedback and measured usability should inform later revisions.', '', '## Review and release', '', 'One pull request holds the full batch plus the previously requested three Science articles. Roger may review and merge the entire PR. The existing github-pages environment approval remains the final publication step. GitHub approval, merge and deployment are different actions; this change does not bypass the release gate.', '', '## Editing', '', 'Edit the nine pipe-separated fields in content/<category>.txt: title, question, materials, three steps separated by " / ", evidence, explanation, extension, safety, reference key. Run `python3 scripts/build_expeditions.py`, then `python3 -m unittest discover -s tests -v`. IDs are assigned by row order; retain that order after publication so shared links remain stable. Refresh the release-readiness record after content changes.', '', '## Inventory', '']
    for category in CATEGORIES:
        review += ['### ' + category, '', '| ID | Expedition |', '| --- | --- |']
        review += [f'| {i["id"]} | {i["title"]} |' for i in items if i['category'] == category]
        review += ['']
    outputs['docs/STEAM-EXPEDITION-REVIEW.md'] = '\n'.join(review) + '\n'
    return outputs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, content in build().items():
        target = ROOT / path
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8') != content:
                raise SystemExit('Generated content is stale: ' + path)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
    print('Verified 125 expeditions: 25 in each STEAM category.' if args.check else 'Built 125 expeditions: 25 in each STEAM category.')

if __name__ == '__main__':
    main()
