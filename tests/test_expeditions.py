"""Catalog completeness, reproducible pages and release integration regressions."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
builder = module('builder', 'scripts/build_expeditions.py')
release = module('release_expeditions', 'scripts/prepare_release.py')

class ExpeditionChecks(unittest.TestCase):
    def test_catalog_contract_and_completeness(self):
        data = json.loads((ROOT / 'assets/expeditions/catalog.json').read_text())
        items = data['expeditions']
        self.assertEqual(len(items), 125)
        self.assertEqual(len({i['id'] for i in items}), 125)
        self.assertEqual(len({i['title'] for i in items}), 125)
        for category in builder.CATEGORIES:
            self.assertEqual(sum(i['category'] == category for i in items), 25)
        for item in items:
            for field in ('question','materials','evidence','explanation','extension','safety','duration'):
                self.assertTrue(item[field].strip(), (item['id'],field))
            self.assertEqual(len(item['steps']), 3)
            self.assertIn(item['source'], data['sources'])
        existing = [i for i in items if i['existing_lesson']]
        self.assertEqual([i['id'] for i in existing], ['TEC-001'])
        self.assertEqual(existing[0]['title'], 'Signals in the Sky')

    def test_generated_pages_are_current(self):
        for path, expected in builder.build().items():
            self.assertEqual((ROOT / path).read_text(encoding='utf-8'), expected, path)

    def test_all_expedition_routes_and_assets_validate(self):
        docs = release.validate_site(ROOT)
        for category in builder.CATEGORIES:
            page = f'expeditions/{category.lower()}.html'
            ids = docs[page].ids
            prefix = builder.PREFIXES[category]
            self.assertTrue(all(f'{prefix}-{n:03}' in ids for n in range(1,26)))

    def test_missing_expedition_anchor_fails_release(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'site'
            shutil.copytree(ROOT, root)
            page = root / 'expeditions/science.html'
            page.write_text(page.read_text().replace('id="SCI-001"', 'id="missing-sci-one"'))
            with self.assertRaisesRegex(ValueError, 'Missing anchor'):
                release.validate_site(root)

    def test_missing_expedition_script_fails_release(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'site'
            shutil.copytree(ROOT, root)
            (root / 'assets/expeditions.js').unlink()
            with self.assertRaisesRegex(ValueError, 'Missing or unsafe local target'):
                release.validate_site(root)

    def test_release_includes_all_catalog_pages_and_portable_data(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest, _ = release.stage_site(ROOT, Path(temp) / 'stage')
            paths = {entry['path'] for entry in manifest}
            self.assertIn('assets/expeditions/catalog.json', paths)
            self.assertTrue(all(f'expeditions/{c.lower()}.html' in paths for c in builder.CATEGORIES))
            self.assertFalse(any(p.startswith(('content/', 'docs/', 'scripts/', 'tests/')) for p in paths))

if __name__ == '__main__':
    unittest.main()
