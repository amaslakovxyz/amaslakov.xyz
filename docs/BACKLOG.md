# Backlog & references

Parked ideas and external references for the amaslakov.{xyz,com} sites.

## References

- **Notion — "Blogging"** (design/reference notes):
  https://app.notion.com/p/amaslak0v/Blogging-3f64a37aabeb48149712664466169bc8

## Backlog (not yet built)

### DevSecOps / security pack
- `/.well-known/security.txt` (RFC 9116).
- Published **PGP public key** + a `/pgp` page.
- "How this site is built & shipped" transparency page (FastAPI → CI → Ansible → systemd).
- Security headers A+ (CSP, HSTS, etc.) + Observatory score link.

### AI & agents
- **"Ask my site"** — RAG chatbot as a terminal command (Claude API). Needs a
  server-side proxy, API key (secret/boundary), rate-limiting; has per-call cost.
- **Agent demos gallery** — agents built, each with an asciinema recording.
- **"Built with agents" colophon** — this site built via Claude Code + CI/Ansible.
- MCP / tools showcase; shareable prompt / agent-config library.

### FDE positioning
- "Work with me" / services page funnelling to the Cal.com booking.
- Case studies / "deployments" (sanitized problem → approach → impact).
- Tech radar (adopt / trial / assess / hold).

### Public presence
- Essays + POSSE syndication (canonical on-site, cross-post to X/LinkedIn).
- TIL / notes stream; JSON-LD `Person` schema + per-page OG; newsletter; webmentions.

### Interactive / flair
- Interactive terminal homepage (type `help`, `ls`, `whoami`, `cat about.md`, `theme …`).
- Command palette (`k` / `/`); extra color schemes; konami-code easter egg.

### Site structure
- **amaslakov.com** — technical CV site, second site in this shared codebase
  (host-based routing). `role`/`now` move here; `.xyz` stays the personal card.
