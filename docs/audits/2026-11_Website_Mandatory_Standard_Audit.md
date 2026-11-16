# Website audit: Mandatory Development Standard v1.1

| | |
| --- | --- |
| Date | 15 November 2026 |
| Standard | ELS-28 Mandatory Development Standard, version 1.1, adopted 26 October 2026. No grandfathering. |
| Related policies | ELS-23 locked wordmark. ELS-22 Engagement Without Exploitation. ELS-21 Source Attribution. ELS-33 About narrative, read with the later ELS-11 mission line. |
| Site | Public development site for Explorers Legacy Studios. Repository `rogercallahan/explorers-legacy-website`, branch reviewed at `0613177` (`main`). GitHub Pages: `https://rogercallahan.github.io/explorers-legacy-website/`. |
| Scope | Home, About, Learn, Sources, Signals in the Sky, the five STEAM expedition pages, shared CSS and scripts, images in the repository, and the release workflow. The Android app, Atlas intro video, and IONOS DNS were not changed. |
| Reviewer | Cursor cloud agent, working under Wall-E as sole AI coordinator (Founder decision of 14 November 2026). This is a review record. It is not Founder acceptance and it does not authorize publication. |
| Method | Source reading, contrast calculation, and rendered checks in Chrome of Home, Learn, About, and a phone-width Home. Items that were not exercised in a browser are marked that way. |

Status words are **pass**, **fail**, or **partial**. A pass is not recorded for behavior this review did not test. Where this change fixes an item, the status is the status after the fix, and the evidence says what was found.

## Locked wordmark (ELS-23)

**Status: pass**, with listed images and video left unchanged.

The standard is EXPLORERS LEGACY in white (`#FFFFFF`) and STUDIOS in Explorer Gold (`#D4AF37`). Ordinary prose is not recolored. Only Roger Callahan or Rebecca Smith may change it.

What this review found:

- STUDIOS was already Explorer Gold in the CSS and on the rendered Home, Learn, and About headers. An earlier teal STUDIOS was corrected on 25 October 2026 (commit `728b628`). The November knowledge summary still listed that correction as open. The rendered line is gold, not teal.
- EXPLORERS LEGACY was maple ivory (`#F4EBD2`) on Home and on the learning masthead, not white. About already used white.
- Learning pages color ordinary links Discovery Teal (`#65d7d0` in `assets/learn.css`). That rule did not override the gold subtitle, but it would paint the wordmark teal if the subtitle color were dropped.

This change sets both lines to the literal standard colors in `index.html`, `about.html`, and `assets/learn.css`, and sets the learning-page brand link itself to white. `assets/expeditions.css` keeps the expedition name line white. A unit test now rejects a teal STUDIOS rule.

### Raster images and video not recolored

These files do not contain the wordmark, or they must not be repainted here:

| File | Why it was left |
| --- | --- |
| `assets/images/els-homepage-hero.png` | Landscape artwork. No wordmark text. |
| `assets/images/els-homepage-hero-test.png.png` | Unreferenced duplicate of the hero. No wordmark. Removing it is a cleanup decision, not a color fix. |
| `assets/images/explorer_compass_circle.png` | Compass emblem. The center gem is teal. That is emblem art, not the wordmark. |
| `assets/images/explorer_compass_icon.png` | Compass emblem. No wordmark. |
| `assets/images/observatory_telescope_icon.png` | Icon. No wordmark. |
| `assets/images/eli_rocket.png` | Icon. No wordmark. |
| `assets/images/signals-pi-setup.jpg` | Project photograph. No wordmark. |
| `assets/images/signals-antenna.jpg` | Project photograph. No wordmark. |
| `assets/images/signals-observed-flight-original.png` | Flightradar24 screenshot kept unedited, with its own credits. No ELS wordmark to recolor. |
| `assets/learn/journey-math.svg`, `sky-perspective.svg`, `transit.svg` | Teaching diagrams. Teal strokes are diagram marks, not the wordmark. |
| Favicon | No favicon file is in the repository. A request for `/favicon.ico` returns 404. Nothing in a favicon was showing STUDIOS in teal. |
| Atlas intro video title card | Not in this repository. The title card is baked into the video and cannot be recolored from the website project. |

## Findings

### 1. The Explorer comes before the engagement metric

**Status: partial.** Severity if left open: low.

Evidence: The About page states the principle in those words. Expeditions tell families to use a paper journal, print the page, and step away. There is no streak, countdown, loot box, points balance, or "your friends are ahead" comparison. Home still shows a gold dot on Learn until that browser opens the highlighted articles (`index.html`, key `els-learn-seen`). The dot is a "new" marker, not a punishment, and the link text changes with it. It is still an attention cue stored on the device. This change documents that storage in the page. Removing the dot is a product decision.

### 2. Curiosity, agency, and a life beyond the screen

**Status: partial.** Severity if left open: medium.

Evidence: Learn articles and the 125 expeditions state a question, an off-screen activity, and a place to explain. `docs/STEAM-EXPEDITION-REVIEW.md` says the activities are starting versions, not field-tested and not a claim of guaranteed learning. Home does not carry that limit. It says the studio "creates meaningful experiences" as a mission sentence, which is not the same as a measured outcome, but a family landing on Home does not see the expedition disclaimer. No child is required to post evidence. Rewards and Discovery Points are not implemented on the site.

### 3. Trustworthy sourcing

**Status: partial.** Severity if left open: medium.

Evidence: Learn articles link to `sources.html` at the point of reading. `assets/learn/sources.json` has 25 entries, each with an `https` URL, and the release check refuses a missing anchor. Thirteen entries have no publication date (`nasa-light-year`, `nasa-transit`, `nasa-voyager-interstellar`, `nasa-voyager-boundary`, `nasa-webb-instruments`, `nasa-voyager-spacecraft`, `voyager-profile-source`, `golden-record-overview`, `golden-record-cover-source`, `voyager-light-day-source`, `orion-distances-source`, `nist-light-speed`, `warwick-green-star`). Review dates and a full permission field are not in the ledger. ELS-21 also asks for creator, material type, required credit line, where it appears, and whether the material is original, observational, a visualization, or a reconstruction.

Signals in the Sky separates a local snapshot from a daily total, labels the Flightradar24 image as used with permission, and says a map sighting does not prove the local receiver supplied the position. That page is in good shape.

Expedition references are optional background links with a privacy warning. Many entries in a category share one general link. That matches the 9 November review note. It is not yet a per-activity source ledger.

Home, the compass, the rocket, the telescope, and the hero have no credit on the page. The Sources page is titled "Sources & Works Cited" rather than "Sources & Acknowledgments." Renaming it is a content decision.

### 4. Responsible AI behavior

**Status: pass.** Not applicable on this site, and the absence is the safe state.

Evidence: No chat, no generated answers, and no claim that Atlas has feelings. Search and print controls in `assets/expeditions.js` run in the browser and do not call a model. TEC-018 is a paper activity about checking an AI answer. It is not an AI feature.

### 5. Child privacy and minimum data

**Status: fail.** Severity: high.

Evidence of what is in good shape: there is no account, no name field, no precise location, no public child profile, and no ELS analytics script. Expedition search text is not saved. The family note says the catalog does not collect journal entries. Arts activities warn against a real child's photograph and identifiable people.

What fails the standard: there is no child-readable notice and no caregiver notice of what happens to a visit. A reader is not told that:

- the Learn marker stores a version string in this browser
- GitHub Pages, the host, can log addresses as part of serving the site
- Learn images are loaded from NASA, ESA, and ESA/Hubble hosts, so opening those articles contacts those services
- outbound links (NASA, ESA, University of Warwick, Flightradar24, the National Gallery of Art, and others) have their own practices

The standard requires that explanation before collection, including for third-party embeds and hosts. This review did not verify GitHub Pages request logs. A notice still has to be written and approved. This change does not add one, because the wording is a Founder decision and a partial notice would understate the third-party requests.

Under-13 consent does not arise for an ELS account, because there is no account. It does not excuse the missing notice about host and third-party requests.

### 6. No tracking or exploitative patterns

**Status: partial.** Severity: low for the pattern, high if a tracker is added later.

Evidence: No `gtag`, pixel, cookie banner, or analytics include in the HTML. No infinite scroll, streak, or paid reward. The only ELS client storage is `localStorage` key `els-learn-seen`. Third-party image hosts can observe requests. That is not an ELS profile, and it is also not "no third-party contact." Do not add analytics to measure the gap.

### 7. Voice, images, location, and inferred traits

**Status: pass.** Not applicable as an ELS feature.

Evidence: The site does not record voice, upload a child's image, read location, or infer emotion. Signals photographs are project photos of equipment, credited to an ELS explorer. The Flightradar24 screenshot is an adult project record, not a child upload.

### 8. Evidence of learning

**Status: partial.** Severity: medium.

Evidence: Expeditions ask for an explanation and a paper product, and they separate that from a score. The review document says they are not field-tested and must not be described as validated learning. No age range is stated. No retention check is claimed. Home does not repeat the limit. Leaving that as a recommendation avoids a homepage rewrite in this change.

### 9. Accessibility

**Status: partial.** Severity: medium for anything still open. The items below that this change touches are closed.

What already held: pages set `lang="en"`. Skip links exist. Header links meet a 44px target. Learn and expedition controls have visible gold focus. Images checked by `scripts/prepare_release.py` have alternative text. Expedition search is labeled. Tables on Signals use row headers.

Contrast against `#0D1B2A`, calculated for this review: white 17.4:1, maple ivory 14.6:1, Explorer Gold `#D4AF37` 8.3:1, Home teal `#2FB6B0` 7.0:1, Learn teal `#65d7d0` 10.1:1. Those pairs meet the usual 4.5:1 text minimum. The Home copyright line is ivory at 50% opacity on `#06111b`, about 4.6:1. It passes with little room. It was not lightened, so the footer color stays as designed.

Fixed here:

- About's skip link landed on the lower article and skipped the page heading. The heading now sits inside `main`.
- Home and About honored `prefers-reduced-motion` only in part or not at all. Both now reduce scroll and transition motion. Learn already did this for its own scroll behavior.
- The Home email address had no underline. It is now underlined, with a visible focus style. About's sources link already had an underline.

Not tested here: a screen reader pass, and a physical phone. Browser checks used a desktop window and a 390px-wide window.

### 10. Mobile navigation

**Status: pass.**

Evidence: Home and About at 390px width showed Home, Games, Learn, About, and Contact, wrapping onto two lines, with targets at least 44px. An older rule set the menu to `display: none` under 900px on Home and under 760px on About. A later rule in the same files turned it back on, which is why the menu was visible. Those hiding rules are removed so a later edit cannot drop the menu by reordering the stylesheet. Learn, Sources, and Signals use the same five links. Expedition pages show Home, Learn, and About only. That shorter menu is visible on a phone-width Science page. Adding Games and Contact there is a navigation choice, not a hidden-menu bug, and it is left for the Founder. This review did not tap every link on a physical phone.

### 11. About page and the foundational narrative

**Status: partial.** Severity: low. This is a wording decision, not a broken page.

ELS-33 is the earlier narrative draft. The recovery note says the later mission is the ELS-11 four-part line, and that later website edits remain source evidence. Roger has treated the About page as official. This change does not rewrite it.

What matches: the curiosity opening, why the studio exists, the Explorer-before-the-metric principle, the compass and True North, no end to discovery, the stepping stone, the legacy continuing, and "Onward to Discovery." The short purpose line and the oath's closing line include "and real-world exploration," which matches ELS-11 rather than the shorter ELS-33 line. Founder approval on 14 November 2026 replaced the oath's "superpower" line with "compass" and added: "Curiosity is our True North. It guides us to explore, to ask why, and to turn the next page." That wording is now on the About page. Home uses "compass" in its shorter True North paragraph and does not repeat the full oath.

What differs:

- The mission card ends in an ellipsis: "To build minds through curiosity, knowledge, play, and real-world exploration by creating meaningful experiences..." The ELS-11 sentence continues: "that inspire exploration, encourage discovery, and empower every Explorer to continue learning beyond the experience itself."
- About adds a sentence that is not in ELS-33: "ELS can provide stepping stones, but we should never pretend we're the whole path. The world around us—and everything that lies beyond it—is part of the classroom."

Completing or cutting either of those is a Founder decision.

### 12. Release and change control

**Status: partial.** Severity: high if someone publishes this branch as if it were approved.

Evidence: `.github/workflows/els-manual-pages-release.yml` deploys only for `rogercallahan`, and only after the github-pages environment approval. `scripts/prepare_release.py` refuses a release when the candidate differs from `.els-release-readiness.json`. That record still points at the earlier STEAM catalog commit. This change does not set it to ready. Tests in this review are the unit tests, not a Founder reading of the pages.

### 13. Custom domain and mail

**Status: pass** for the current site, with a standing constraint.

Evidence: There is no `CNAME` file and this change does not add one. The development site stays on GitHub Pages. DNS was not changed.

Standing constraint, from the Founder's project record: `explorerslegacystudios.com` (primary), the `.org`, and `explorerslegacyinstitute.com` are on IONOS. Mail for `info@explorerslegacystudios.com` is on IONOS. The IONOS dashboard has wrongly said that no mailbox exists. When the domain is connected, the IONOS MX records must be preserved. Connecting the domain is out of scope until the Founder asks for it.

### 14. Durable guidance for the next worker

**Status: pass** after this change.

Evidence: The repository had no `AGENTS.md`. This change adds one and links this audit from it and from the README. That is the "next work session" step in section 8 of the standard. It does not adopt the Operational Standard, which is still not the controlled master, and it does not amend the Constitution.

## Prioritized remaining work

These need the Founder. They are not done in this change.

1. **High. Privacy notice.** Approve a short child-readable note and a caregiver note: no name or account is requested; the Learn marker stores only a version string in the browser; GitHub Pages may log requests; Learn images and outbound links contact other sites. Say how to clear the marker (clear site data for this browser).
2. **High. Third-party images.** Decide whether Learn should keep hotlinking NASA, ESA, and Hubble images. Hotlinking avoids copying files the studio may not have a license to store, and it also sends the reader's address to those hosts. Self-hosting needs a license check and credits. Do not add an analytics tool while deciding.
3. **High. Do not publish this audit as a launch.** Merges and GitHub Pages publication still need the Founder's approval. Leave the readiness record on hold until that review.
4. **Medium. About mission sentence.** Decide whether to finish the ellipsis with the ELS-11 mission sentence, and whether the extra "whole path" sentence stays.
5. **Medium. Source ledger.** Add missing publication dates, review dates, and the ELS-21 fields (creator, permission, credit line, where used, material type). Credit the hero, compass, rocket, and telescope, or record them as original ELS art if that is what they are.
6. **Medium. Homepage limit.** Decide whether Home should quietly say that expeditions are family starting points and have not been field-tested, so the public page matches the expedition review.
7. **Low. Learn "new" dot.** Keep it, or remove it if a marker that waits to be clicked is more attention design than the studio wants.
8. **Low. Intro video.** Recut the Atlas intro title card to white and Explorer Gold in the video project. It is not in this website repository.
9. **Low. Unused hero duplicate.** `assets/images/els-homepage-hero-test.png.png` is unreferenced. Delete it only if it is not needed as a reference file.
10. **Standing. DNS.** When the custom domain is connected, preserve the IONOS MX records. Do not connect it in a website pull request.

## What this change did

- Locked the on-screen wordmark to white and `#D4AF37`, and stopped the learning-page link color from being able to paint it.
- Removed the contradictory rules that hid the phone menu and then showed it again.
- Pointed the About skip link at the heading.
- Honored reduced motion on Home and About, and underlined the Home email address.
- Documented the Learn marker's browser storage.
- Added `AGENTS.md`, this audit, a README pointer, and a wordmark color test.
- Did not rewrite About, did not add a privacy essay, did not recolor emblem art or photographs, did not connect a domain, and did not mark the release record ready.
