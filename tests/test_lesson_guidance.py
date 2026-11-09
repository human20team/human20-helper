from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require_lesson_guidance(text: str) -> None:
    required = (
        'get_section(section="lessons", workshop_id=RESOLVED_WORKSHOP_ID)',
        'get_content_detail(item_id=CATALOG_ITEM_ID, workshop_id=RESOLVED_WORKSHOP_ID)',
        'Never construct lesson IDs from numbers.',
        'including `jun-` versus `june-`',
        'Do not regenerate tokens or grant another workshop to hide an ID mismatch.',
        'legacy numbered shortcuts',
        'references/lesson-content-access.md',
    )
    for rule in required:
        if rule not in text:
            raise AssertionError(f'Missing lesson guidance: {rule}')
    if text.index(required[0]) > text.index(required[1]):
        raise AssertionError('Catalog discovery must precede detail retrieval')


class LessonGuidanceTest(unittest.TestCase):
    def test_required_workflow_is_loaded_from_skill_root(self):
        require_lesson_guidance((ROOT / 'SKILL.md').read_text())

    def test_missing_critical_rule_is_rejected(self):
        text = (ROOT / 'SKILL.md').read_text()
        for rule in ('Never construct lesson IDs from numbers.',
                     'Do not regenerate tokens or grant another workshop to hide an ID mismatch.'):
            with self.subTest(rule=rule), self.assertRaises(AssertionError):
                require_lesson_guidance(text.replace(rule, ''))

    def test_reference_examples_preserve_scoped_nonuniform_ids(self):
        text = (ROOT / 'references/lesson-content-access.md').read_text()
        calls = [(tool, json.loads(args)) for tool, args in re.findall(
            r"--tool (get_section|get_content_detail) --args '([^']+)'", text)]
        self.assertEqual(calls[0], ('get_section', {
            'section': 'lessons', 'workshop_id': 'human20-codex-hermes'}))
        self.assertEqual([args['item_id'] for tool, args in calls[1:]],
                         ['june-lesson-4', 'jun-lesson-5', 'jun-lesson-6'])
        self.assertTrue(all(tool == 'get_content_detail' and
                            args['workshop_id'] == 'human20-codex-hermes'
                            for tool, args in calls[1:]))
        self.assertIn('Only if the current catalog confirms these IDs', text)

    def test_guidance_is_linked_from_both_entry_documents(self):
        for name in ('SKILL.md', 'README.md'):
            with self.subTest(document=name):
                self.assertIn('(references/lesson-content-access.md)', (ROOT / name).read_text())


if __name__ == '__main__':
    unittest.main()
