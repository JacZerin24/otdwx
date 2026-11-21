"""Unit tests for source-dependent, hazard-specific OTDwx theme renderings."""
import copy
from xml.etree import ElementTree
import unittest

from otdwx.themed_graphics import THEMES, render_themed, validate_themed


def package(theme, typ='big_number', spec=None):
    if spec is None:
        spec={'title': 'Test only / not historical', 'hero':'25',
              'hero_label':'invented unit test', 'detail_lines':['No observed data']}
    return {'event_date':'1900-01-01', 'source_name':'FICTIONAL TEST SOURCE',
            'alt':'Test fixture with no actual meteorological observation or event.',
            'type':typ,'weather_category':theme, 'graphic_spec':copy.deepcopy(spec)}


class ThemeV3Tests(unittest.TestCase):
    def test_theme_specific_palettes_and_mastheads(self):
        self.assertEqual(10,len(THEMES))
        self.assertEqual(10,len({t.accent for t in THEMES.values()}))
        for key,theme in THEMES.items():
            with self.subTest(theme=key):
                item=package(key)
                svg=render_themed(item)
                ElementTree.fromstring(svg)
                self.assertIn(theme.label,svg)
                self.assertIn(theme.paper,svg)
                self.assertIn('SOURCE: FICTIONAL TEST SOURCE',svg)
                self.assertNotIn('<image',svg)

    def test_xml_escape_and_headline_length_validation(self):
        x=package('winter',spec={'title':'Test <&> snowfall',
                                  'hero':'8','hero_label':'test'})
        self.assertIn('Test &lt;&amp;&gt; snowfall',render_themed(x))
        x['graphic_spec']['title']='LONGNAME '*20
        self.assertTrue(validate_themed(x))

    def test_numeric_comparison(self):
        x=package('temperature','bar_comparison',{'title':'Test heat comparison',
            'rows':[{'label':'Year A','value':114},{'label':'Year B','value':106}], 'unit':'°F'})
        self.assertEqual([],validate_themed(x))
        self.assertIn('114 °F',render_themed(x))
        x['graphic_spec']['rows'][0]['value']=float('nan')
        self.assertTrue(validate_themed(x))

    def test_track_map_requires_sourced_points_and_label(self):
        spec={'title':'TEST approximate path','bounds':[-92,29,-88,32],
              'track':[[-91,29.5],[-90,30.5]],'track_quality':'approximate'}
        x=package('tornado','track_map',spec)
        self.assertTrue(validate_themed(x))
        x['graphic_spec']['data_source_url']='https://example.org/fixture'
        self.assertEqual([],validate_themed(x))
        svg=render_themed(x)
        ElementTree.fromstring(svg)
        self.assertIn('APPROXIMATE PATH',svg)
        self.assertIn('stroke-dasharray',svg)
        x['graphic_spec']['track'][1]=[-180,89]
        self.assertTrue(validate_themed(x))

    def test_point_map_requires_observation_source(self):
        spec={'title':'TEST observations','bounds':[-92,29,-88,32],
             'points':[{'label':'Gauge A','coordinates':[-90,30]}]}
        x=package('flood','point_map',spec)
        self.assertTrue(validate_themed(x))
        x['graphic_spec']['data_source_url']='https://example.org/fixture'
        self.assertEqual([],validate_themed(x))
        self.assertIn('Gauge A',render_themed(x))

    def test_override_theme_and_invalid_override(self):
        x=package('winter')
        x['graphic_spec']['theme']='tropical'
        self.assertIn('TROPICAL / CYCLONE',render_themed(x))
        x['graphic_spec']['theme']='disco_snow'
        self.assertTrue(validate_themed(x))

    def test_radar_theme_validation_and_palette(self):
        from otdwx.radar_loop import validate_manifest
        spec={'title':'Synthetic','source_name':'Test','source_url':'https://example.org/radar',
              'radar_site':'KXXX','product':'test','weather_category':'tropical',
              'media_rights_reviewed':True,'data_provenance_reviewed':True,
              'frames':[{'file':'a.png','timestamp_utc':'2020-01-01T00:00:00Z'},
                        {'file':'b.png','timestamp_utc':'2020-01-01T00:05:00Z'}]}
        self.assertEqual([],validate_manifest(spec))
        spec['weather_category']='supercell_rainbow'
        self.assertTrue(validate_manifest(spec))

    def test_all_old_visual_types_have_v3(self):
        examples={
            'contrast':{'title':'Test','left':{'name':'A','value':'1'},'right':{'name':'B','value':'2'}},
            'morning_timeline':{'title':'Test','hero':'2 h','start':'10 AM','end':'12 PM'},
            'warning_timeline':{'title':'Test','hero':'15 min','start':'10 AM','end':'12 PM'},
            'conceptual_schematic':{'title':'Test','upper':'WARM','middle':'COOL'},
        }
        for typ,spec in examples.items():
            with self.subTest(typ=typ):
                x=package('unusual',typ,spec)
                self.assertEqual([],validate_themed(x))
                ElementTree.fromstring(render_themed(x))


if __name__ == '__main__':
    unittest.main()