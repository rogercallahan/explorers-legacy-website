"""Validate and stage the ELS site; keep publication behind Roger's environment approval."""
import argparse, hashlib, json, os, pathlib, re, shutil, subprocess
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

PAGES = ('index.html', 'about.html', 'learn.html', 'sources.html')
RECORD = '.els-release-readiness.json'

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.images = set(), [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                raise ValueError('Duplicate HTML id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag == 'img':
            if 'alt' not in a:
                raise ValueError('Image missing alternative text')
            self.images.append(a.get('src', ''))

def validate_site(root):
    docs = {}
    for name in PAGES:
        doc = Document()
        doc.feed((root / name).read_text(encoding='utf-8'))
        docs[name] = doc
    for name, doc in docs.items():
        for url in doc.links + doc.images:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                if parsed.scheme not in ('https', 'http', 'mailto', 'tel'):
                    raise ValueError('Unsupported URL scheme: ' + url)
                continue
            target = (root / name).parent / unquote(parsed.path) if parsed.path else root / name
            target = target.resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                raise ValueError('Missing or unsafe local target: ' + name + ': ' + url)
            if parsed.fragment and target.suffix == '.html':
                key = target.relative_to(root.resolve()).as_posix()
                if key not in docs or unquote(parsed.fragment) not in docs[key].ids:
                    raise ValueError('Missing anchor: ' + name + ': ' + url)
    registry = json.loads((root / 'assets/learn/sources.json').read_text(encoding='utf-8'))
    ids = [entry['id'] for entry in registry]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate source registry id')
    for entry in registry:
        if entry['id'] not in docs['sources.html'].ids or not entry['url'].startswith('https://'):
            raise ValueError('Source entry missing or invalid: ' + entry['id'])
    return docs

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()

def readiness(root, candidate):
    record = json.loads((root / RECORD).read_text(encoding='utf-8'))
    if record.get('status') != 'ready':
        return False, record
    reviewed = record.get('reviewed_commit', '')
    if not re.fullmatch(r'[0-9a-f]{40}', reviewed):
        raise ValueError('Readiness must identify the exact reviewed commit')
    # Any change outside the assessment record invalidates the concurrence.
    changed = git(root, 'diff', '--name-only', reviewed, candidate).splitlines()
    if any(p != RECORD for p in changed):
        raise ValueError('Candidate differs from the reviewed content; fresh review required')
    subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', reviewed, candidate], check=True)
    for key in ('atlas_concurrence', 'verification', 'recovery'):
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError('Missing readiness evidence: ' + key)
    if not re.fullmatch(r'[0-9a-f]{40}', record.get('known_good_commit', '')):
        raise ValueError('Missing known-good recovery commit')
    subprocess.run(['git', '-C', str(root), 'cat-file', '-e', record['known_good_commit'] + '^{commit}'], check=True)
    return True, record

def stage_site(root, dest):
    dest.mkdir(parents=True, exist_ok=False)
    for name in (*PAGES, 'assets'):
        source = root / name
        if source.is_symlink() or (source.is_dir() and any(p.is_symlink() for p in source.rglob('*'))):
            raise ValueError('Website payload must not contain symbolic links')
        if source.is_dir():
            shutil.copytree(source, dest / name)
        else:
            shutil.copyfile(source, dest / name)
    manifest = [{'path': p.relative_to(dest).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in sorted(dest.rglob('*')) if p.is_file()
                and not any(part.startswith('.') for part in p.relative_to(dest).parts)]
    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return manifest, digest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=pathlib.Path)
    parser.add_argument('--release', action='store_true')
    args = parser.parse_args()
    root = pathlib.Path.cwd()
    validate_site(root)
    candidate = os.environ.get('GITHUB_SHA') or (git(root, 'rev-parse', 'HEAD') if args.release else 'local-preview')
    ready, record = readiness(root, candidate) if args.release else (False, {})
    manifest, digest = stage_site(root, args.stage) if args.stage else ([], '')
    output = os.environ.get('GITHUB_OUTPUT')
    if output:
        with open(output, 'a', encoding='utf-8') as stream:
            stream.write('ready=' + str(ready).lower() + '\n')
            stream.write('payload_sha256=' + digest + '\n')
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        reference = 'https://github.com/rogercallahan/explorers-legacy-website/blob/' + candidate + '/' + RECORD
        with open(summary, 'a', encoding='utf-8') as stream:
            stream.write('# ELS release review\n\n')
            stream.write('Candidate: `' + candidate + '`\n\n')
            stream.write('[Readiness and recovery record](' + reference + ')\n\n')
            stream.write('Atlas readiness: ' + ('ready' if ready else 'on hold / preview only') + '\n\n')
            stream.write('Roger’s approval of the github-pages deployment is final publication authorization for this candidate and artifact.\n\n')
            stream.write('Payload manifest SHA-256: `' + digest + '`\n\n')
            stream.write('File hashes:\n\n```json\n' + json.dumps(manifest, indent=2) + '\n```\n')
    print('Website references and assets validated. Publication readiness:', ready)

if __name__ == '__main__':
    main()
