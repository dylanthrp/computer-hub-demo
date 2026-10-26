import unittest, json, sys, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import render

class BuildTests(unittest.TestCase):
    def setUp(self): self.data=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
    def test_generated_matches(self): self.assertEqual((ROOT/'index.html').read_text(encoding='utf-8'),render(self.data))
    def test_confirmed_contact_fields(self):
        page=render(self.data)
        self.assertIn('href="tel:+13134519200"',page)
        self.assertIn('href="mailto:info@thecomputerhub.net"',page)
        self.assertIn('22222 Van Born Road, Dearborn Heights, MI',page)
        self.assertIn('href="https://thecomputerhub.net/"',page)
        self.assertIn('Computer repair service',page)
        self.assertIn('Computer store',page)
        self.assertEqual(self.data['hours'],[])
        self.assertNotIn('id="about"',page)
        self.assertIn('noindex,nofollow',page)
    def test_approved_future_sections(self):
        page=render(self.data)
        self.assertIn('Slow computer?',page)
        self.assertIn('Broken screen?',page)
        self.assertIn('Call the Shop',page)
        self.assertIn('assets/typing-reference.webp',page)
        self.assertIn('assets/typing-reference.jpg',page)
        self.assertIn('width="620" height="770"',page)
        self.assertIn('Illustrative typing photo',page)
        self.assertIn('id="owner-note"',page)
        self.assertIn('working demo, not a final design',page)
        self.data['offerings']=[{'title':'TEST ONLY','description':'Fixture text'}]
        self.data['about']={'heading':'TEST ONLY','description':'Fixture text'}
        page=render(self.data)
        self.assertIn('id="offerings"',page);self.assertIn('href="#offerings"',page)
        self.assertIn('id="about"',page)
    def test_html_escape(self):
        self.data['hero']['description']='<script>alert("test")</script>'
        self.assertNotIn('<script>alert',render(self.data))
        self.assertIn('&lt;script&gt;',render(self.data))
    def test_zero_one_many_photos(self):
        self.assertNotIn('class="photo-slider"',render(self.data))
        photo={'webp':'assets/test-only.webp','fallback':'assets/test-only.jpg','width':1200,'height':900,'alt':'TEST ONLY'}
        self.data['photos']=[photo]
        self.assertIn('class="photo-slider"',render(self.data));self.assertNotIn('data-next',render(self.data))
        self.data['photos']=[copy.deepcopy(photo) for _ in range(5)]
        page=render(self.data)
        self.assertEqual(page.count('class="slide"'),4);self.assertIn('data-next',page)
    def test_original_preserved(self):
        source=Path('C:/Users/dylan/Documents/vecchione-chiro-demo/.hermes/desktop-attachments/471727299_122203546028225619_4860440700260907635_n.jpg')
        if not source.exists(): self.skipTest('External original source is not available on this machine')
        self.assertEqual(source.read_bytes(),(ROOT/'assets/originals'/source.name).read_bytes())
    def test_contact_fields_generated_from_one_source(self):
        self.data['phone']={'display':'Test-only number','e164':'+12025550123'}
        self.data['email']='test@example.com'
        self.data['hours']=[{'day':'Test day','time':'Test hours'}]
        page=render(self.data)
        self.assertEqual(page.count('href="tel:' + self.data['phone']['e164'] + '"'),4)
        self.assertIn('href="mailto:test@example.com"',page)
        self.assertIn('Test hours',page)

if __name__=='__main__':unittest.main()
