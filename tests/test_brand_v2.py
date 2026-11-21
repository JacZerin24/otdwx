import tempfile
from pathlib import Path
from xml.etree import ElementTree
import unittest

from otdwx.branded_graphics import render_visual, validate_visual
from otdwx.radar_loop import validate_manifest, render_gif


def sample(typ, graphic_spec):
    return {'type':typ,'event_date':'2022-11-20','source_name':'Example Archive',
            'alt':'Source-backed observed data: a synthetic example for tests only.',
            'graphic_spec':graphic_spec}


class BrandV2Tests(unittest.TestCase):
    def test_comparison_renders_valid_standalone_svg(self):
        pkg=sample('bar_comparison',{'title':'Fictional <storm>','subtitle':'Test only',
                 'rows':[{'label':'2022','value':30.2},{'label':'1951','value':23.4}],
                 'unit':'in','footnote':'Example only'})
        self.assertEqual([],validate_visual(pkg))
        svg=render_visual(pkg)
        self.assertIn('&lt;storm&gt;',svg)
        self.assertNotIn('<image',svg)
        ElementTree.fromstring(svg)

    def test_regional_track_map_rejects_unsourced_data(self):
        spec={'title':'TEST','bounds':[-91,28,-89,31],
              'track':[[-90.5,29],[-90.1,30]],'track_quality':'surveyed'}
        self.assertTrue(any('source' in s for s in validate_visual(sample('track_map',spec))))
        spec['data_source_url']='https://example.org/record'
        pkg=sample('track_map',spec)
        self.assertEqual([],validate_visual(pkg))
        ElementTree.fromstring(render_visual(pkg))
        spec['track'][1]=[-200,40]
        self.assertTrue(validate_visual(pkg))

    def test_point_map_genuine_observation_schema(self):
        pkg=sample('point_map',{'title':'TEST','bounds':[-92,28,-88,32],
                    'data_source_url':'https://example.org/data',
                    'points':[{'coordinates':[-90.5,30.1],'label':'Station A'}]})
        self.assertEqual([],validate_visual(pkg))
        self.assertIn('Station A',render_visual(pkg))

    def test_six_legacy_types_supported_in_brand(self):
        specs={'big_number':{'title':'Synthetic','hero':'82','hero_label':'mph'},
               'contrast':{'title':'Two sites','left':{'name':'A','value':'1'},
                           'right':{'name':'B','value':'2'}},
               'morning_timeline':{'title':'Timeline','hero':'1h','start':'5 AM','end':'6 AM'},
               'warning_timeline':{'title':'Timeline','hero':'17min','start':'5 AM','end':'6 AM'},
               'conceptual_schematic':{'title':'Conceptual','upper':'Inversion'}}
        for typ,spec in specs.items():
            with self.subTest(typ=typ):
                pkg=sample(typ,spec)
                self.assertEqual([],validate_visual(pkg))
                ElementTree.fromstring(render_visual(pkg))

    def test_radar_manifest_requires_provenance_and_utc(self):
        spec={'title':'Synthetic radar', 'source_name':'Example Archive',
              'source_url':'https://example.org/radar', 'radar_site':'KXXX',
              'product':'0.5 deg reflectivity','frames':[
                {'file':'frame1.png','timestamp_utc':'2022-01-01T00:00:00Z'},
                {'file':'frame2.png','timestamp_utc':'2022-01-01T00:05:00Z'}]}
        self.assertTrue(validate_manifest(spec))
        spec['media_rights_reviewed']=spec['data_provenance_reviewed']=True
        self.assertEqual([],validate_manifest(spec))
        spec['frames'].reverse()
        self.assertTrue(validate_manifest(spec))

    def test_gif_from_real_rendered_frame_path_fixture(self):
        try:from PIL import Image
        except ImportError:self.skipTest('optional Pillow not installed')
        with tempfile.TemporaryDirectory() as d:
            for i in range(2):
                Image.new('RGB',(160,100),'#f0f0f0').save(Path(d)/f'f{i}.png')
            spec={'title':'SYNTHETIC TEST ONLY','source_name':'Example Archive',
                'source_url':'https://example.org/radar','radar_site':'KXXX',
                'product':'simulated-fixture','media_rights_reviewed':True,
                'data_provenance_reviewed':True,'frames':[
                    {'file':'f0.png','timestamp_utc':'2022-01-01T00:00:00Z'},
                    {'file':'f1.png','timestamp_utc':'2022-01-01T00:05:00Z'}]}
            out=render_gif(spec,Path(d)/'demo.gif',root=d)
            with Image.open(out) as img:self.assertEqual(img.n_frames,2)

if __name__=='__main__':unittest.main()
