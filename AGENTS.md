# AGENTS.md

Guidance for AI workers on the Explorers Legacy Studios website. This file does not replace the adopted Mandatory Development Standard. It tells workers what is already decided.

## Authority

Roger Callahan is the final authority. Rebecca Smith shares authority over the locked wordmark only.

Wall-E is the sole AI coordinator, by Founder decision of November 14, 2026. Workers may implement, test, diagnose, and propose inside an assigned task. Workers may not merge, publish, redefine the brand, educational philosophy, architecture, or objectives, or accept new work on their own.

Merges to `main` and publishing to GitHub Pages need the Founder's approval. A passing test run is not approval. Do not mark `.els-release-readiness.json` ready unless the Founder has reviewed that exact commit.

Do not connect `explorerslegacystudios.com`, the `.org`, or `explorerslegacyinstitute.com`, and do not change DNS. When a domain is eventually connected, the IONOS MX records must be preserved so `info@explorerslegacystudios.com` keeps working. The IONOS dashboard has been wrong about that mailbox existing. See the November 2026 audit.

## Locked wordmark (ELS-23)

In the visual wordmark:

- **EXPLORERS LEGACY** is white, `#FFFFFF`.
- **STUDIOS** is Explorer Gold, `#D4AF37`.

Ordinary sentences that mention Explorers Legacy Studios do not use this color treatment. Only Roger Callahan or Rebecca Smith may change the wordmark. Discovery Teal is a palette color for other interface text. It must not color STUDIOS.

## Mandatory Development Standard, version 1.1

Adopted October 26, 2026. There is no grandfathering. Work from before that date still has to be reviewed. The governing principle is: **the Explorer comes before the engagement metric.**

What that requires on this website:

1. Learning comes before time-on-site. No streaks, punishment for leaving, artificial countdowns, social pressure, loot boxes, or notifications whose job is to pull a child back.
2. Expeditions keep a real-world path where it fits: ask or predict, investigate or build, explain independently, check a credited source, and keep only the evidence that is needed. A paper journal is enough. Do not require a child to post proof publicly.
3. Factual teaching needs a traceable source: URL, date when one exists, review date, and who owns the content. Say what is verified, what is a claim, and what is still uncertain. Do not invent citations or treat an AI answer as evidence.
4. Do not collect a child's name or other personal data the page does not need. There is no child name field. Address the reader as Explorer. Location, public profiles, behavioral profiling, and third-party sharing stay off. Anything collected needs a purpose, a retention period, a way to delete it, and an owner.
5. Explain collection in language a child can read, with a fuller note for caregivers. Verified caregiver consent is required before personal data is collected from anyone under 13, except a narrow case the law actually allows and the project has written down.
6. Child data is not for targeted advertising, commercial profiling, or training general-purpose AI models.
7. There is no conversational Atlas on this site. If one is added later, it must not claim human feelings, ask a child to keep secrets, or use dependence to hold attention. Generated facts need an approved source or a clear statement that they cannot be checked.
8. Do not describe a page as a validated educational or diagnostic assessment. Participation is not the same thing as mastery. This catalog has not been field-tested with children.
9. Third-party scripts, analytics, embeds, fonts, and image hosts get the same privacy review as ELS code. Do not add trackers.
10. Accessibility is part of the work: keyboard access, visible focus, text alternatives, contrast, reduced motion, and a navigation path on a phone.
11. A material change needs a short review record. Untested behavior is not a pass. Safety, privacy, or misleading-claim failures block release of the affected page.
12. New agents read this file and the audit before editing.

The November 2026 review is [docs/audits/2026-11_Website_Mandatory_Standard_Audit.md](docs/audits/2026-11_Website_Mandatory_Standard_Audit.md).

## How to change this site

- Work on a branch and open a pull request. Do not commit to `main`.
- Stay inside the assigned task. Recommend large content or design changes. Do not make them quietly.
- Do not commit secrets.
- Before a pull request, run `python3 -m unittest discover -s tests -v`.
- The GitHub Pages workflow publishes only after the Founder's environment approval, and only when the readiness record matches the reviewed commit. Do not bypass it.
