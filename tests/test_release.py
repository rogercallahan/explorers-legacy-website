import importlib.util, json, pathlib, shutil, subprocess, tempfile, unittest
SITE = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('release', SITE / 'scripts/prepare_release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)

class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        (self.root / 'index.html').write_text('reviewed content')
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Release checks')
        self.git('add', '.')
        self.git('commit', '-qm', 'Reviewed source')
        self.reviewed = self.git('rev-parse', 'HEAD')
        self.record = dict(status='ready', reviewed_commit=self.reviewed,
            atlas_concurrence='Reviewed', verification='Checked', recovery='Restore through reviewed PR',
            known_good_commit=self.reviewed)
    def tearDown(self):
        self.temp.cleanup()
    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True).strip()
    def commit_record(self):
        (self.root / release.RECORD).write_text(json.dumps(self.record))
        self.git('add', '.')
        self.git('commit', '-qm', 'Record assessment')
        return self.git('rev-parse', 'HEAD')
    def test_only_record_change_is_ready(self):
        self.assertTrue(release.readiness(self.root, self.commit_record())[0])
    def test_hold_never_authorizes(self):
        self.record['status'] = 'hold'
        self.assertFalse(release.readiness(self.root, self.commit_record())[0])
    def test_changed_content_rejected(self):
        (self.root / 'index.html').write_text('unreviewed content')
        candidate = self.commit_record()
        with self.assertRaisesRegex(ValueError, 'differs'):
            release.readiness(self.root, candidate)
    def test_malformed_commit_rejected(self):
        self.record['reviewed_commit'] = 'main'
        with self.assertRaisesRegex(ValueError, 'exact reviewed'):
            release.readiness(self.root, self.commit_record())
    def test_missing_concurrence_rejected(self):
        self.record['atlas_concurrence'] = ''
        with self.assertRaisesRegex(ValueError, 'Missing readiness'):
            release.readiness(self.root, self.commit_record())
    def test_reference_integrity(self):
        release.validate_site(SITE)
        shutil.copytree(SITE, self.root / 'site')
        sources = self.root / 'site/sources.html'
        sources.write_text(sources.read_text(encoding='utf-8').replace('id="nasa-transit"', 'id="removed-transit"'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Missing anchor'):
            release.validate_site(self.root / 'site')
    def test_staged_payload_excludes_workflow(self):
        manifest, digest = release.stage_site(SITE, self.root / 'stage')
        paths = {m['path'] for m in manifest}
        self.assertTrue(set(release.PAGES).issubset(paths))
        self.assertFalse(any(p.startswith(('.github', 'scripts')) for p in paths))
        self.assertEqual(len(digest), 64)

if __name__ == '__main__':
    unittest.main(verbosity=2)
