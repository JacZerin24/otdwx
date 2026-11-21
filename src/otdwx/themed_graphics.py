"""OTDwx Visual System v3 — hazard-specific editorial SVGs.

A consistent small masthead, event dateline and source line identify the brand;
typography, composition and sourced-data marks adapt to the hazard. The vector
motifs are *decorative*, not recreations of actual weather imagery. No external
images, embedded pixels, invented geographies or external dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from html import escape
import math
import textwrap
from urllib.parse import urlparse

W, H = 1600, 900

@dataclass(frozen=True)
class Theme:
    name: str
    label: str
    paper: str
    ink: str
    accent: str
    secondary: str
    faint: str
    muted: str
    rule: str
    dark: bool = False

THEMES = {
    'winter': Theme('winter','WINTER / SNOW','#ecf3f5','#122a40','#127aa3','#73b5d1','#d9e6ec','#5d7485','#b8cbd4'),
    'tornado': Theme('tornado','TORNADO / SURVEY','#f3ede4','#292724','#b53c2a','#d9a45d','#e8dacf','#706860','#c6b6a6'),
    'severe_storm': Theme('severe_storm','SEVERE / CONVECTIVE','#192333','#f8f1e5','#ffcc5a','#e4775c','#26394a','#bfc7ce','#55616c',True),
    'tropical': Theme('tropical','TROPICAL / CYCLONE','#0d2c3e','#f4f0e5','#49baa7','#f8b772','#174358','#b6cfd2','#416c76',True),
    'flood': Theme('flood','FLOOD / HYDROLOGY','#eaf1ef','#172f32','#147f91','#6ebfb8','#d1e4e3','#617779','#afc9c7'),
    'temperature': Theme('temperature','TEMPERATURE / RECORD','#fbf1e4','#3a2823','#c34c32','#ebac5c','#f4dcc5','#906d63','#dcc5b3'),
    'drought': Theme('drought','DROUGHT / CLIMATE','#f5eedf','#413629','#a26a34','#cfaf79','#e7dcc6','#8e806c','#d3c4ac'),
    'wildfire_weather': Theme('wildfire_weather','FIRE WEATHER / WIND','#282221','#faf0e4','#f38c51','#c75135','#3e302b','#d4bbb0','#70544a',True),
    'unusual': Theme('unusual','ATMOSPHERIC / HISTORY','#eeeff2','#272b3b','#6a5c99','#a1b5cb','#e0e3ea','#777c91','#c3c8d5'),
    'other': Theme('other','THE WEATHER ARCHIVE','#f2f0e9','#23353e','#187b87','#b58b5e','#dce2df','#6e7d7c','#c8cdca'),
}
ALIASES = {
    'snow':'winter','ice':'winter','blizzard':'winter','cold':'winter',
    'severe':'severe_storm','thunderstorm':'severe_storm','hail':'severe_storm',
    'hurricane':'tropical','typhoon':'tropical','cyclone':'tropical',
    'rain':'flood','flash_flood':'flood','heat':'temperature','heatwave':'temperature',
    'wildfire':'wildfire_weather','fire_weather':'wildfire_weather','fog':'unusual',
}
TYPES = {'bar_comparison','big_number','contrast','morning_timeline','warning_timeline',
         'conceptual_schematic','track_map','point_map'}


def _s(value):
    return escape(str(value), quote=True)


def _text(x,y,value,size=24,color=None,weight='normal',family='sans',anchor='start',spacing=0):
    font = "Georgia,'Times New Roman',serif" if family == 'serif' else "Arial,Helvetica,sans-serif"
    return (f'<text x="{x:g}" y="{y:g}" fill="{color}" font-size="{size:g}" '
            f'font-family="{font}" font-weight="{weight}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}">{_s(value)}</text>')


def _rect(x,y,w,h,fill,r=0):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"/>'


def _line(x1,y1,x2,y2,color,width=2,dash=''):
    return (f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
            f'stroke="{color}" stroke-width="{width:g}"'+
            (f' stroke-dasharray="{dash}"' if dash else '')+'/>')


def _circle(cx,cy,r,fill='none',stroke='none',sw=1):
    return f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}"/>'


def _path(d,stroke,sw=2,fill='none',opacity=None):
    return f'<path d="{d}" stroke="{stroke}" stroke-width="{sw:g}" fill="{fill}"'+(f' opacity="{opacity:g}"' if opacity else '')+'/>'


def _lines(value,max_chars,limit=2):
    value=str(value).strip()
    if not value:return []
    output=[]
    for para in value.split('\n'):
        output += textwrap.wrap(para, width=max_chars,break_long_words=False,
                                break_on_hyphens=False) or ['']
    if len(output)>limit:
        raise ValueError('Graphic headline/annotation too long for the chosen layout; shorten it')
    return output


def _stack(parts,x,y,value,width,size,leading,theme,*,color=None,family='serif',weight='bold',limit=2):
    for i,ln in enumerate(_lines(value,width,limit)):
        parts.append(_text(x,y+i*leading,ln,size,color or theme.ink,weight,family))


def _theme(item):
    spec=item['graphic_spec']
    choice=spec.get('theme') or item.get('weather_category') or item.get('weather_type') or 'other'
    choice=ALIASES.get(choice,choice)
    if choice not in THEMES:raise ValueError('Unknown weather theme '+str(choice))
    return THEMES[choice]


def _ornament(t):
    """Clearly decorative marks: not simulated observations or location data."""
    pieces=[]
    if t.name=='winter':
        # Negative-space snow crystals and drifting lines, NOT a weather map.
        for k,(cx,cy,r) in enumerate([(1430,258,78),(1340,572,48),(1510,665,45)]):
            for a in range(0,360,60):
                theta=math.radians(a)
                dx=r*math.cos(theta);dy=r*math.sin(theta)
                pieces.append(_line(cx-dx,cy-dy,cx+dx,cy+dy,t.secondary,2))
                for direction in (-1,1):
                    ex=cx+direction*dx;ey=cy+direction*dy
                    for off in (-22,22):
                        beta=theta+direction*math.pi+math.radians(off)
                        pieces.append(_line(ex,ey,ex+19*math.cos(beta),ey+19*math.sin(beta),t.secondary,2))
        pieces.append(_path('M 1200 790 C 1320 754 1430 810 1600 760',t.secondary,4,opacity=.35))
    elif t.name=='tornado':
        for i in range(17):
            x=1210+17*i
            pieces.append(_line(x,275,x+170,545,t.rule,2))
        pieces.append(_path('M 1270 610 C 1340 620 1440 590 1500 630',t.accent,5,opacity=.45))
        pieces.append(_text(1440,758,'SURVEY  /  ARCHIVE',18,t.muted,'bold',anchor='middle',spacing=2))
    elif t.name=='severe_storm':
        for y in range(283,750,45):
            pieces.append(_line(1230,y,1540,y,t.rule,1))
        for x in range(1230,1550,37):
            pieces.append(_line(x,280,x,750,t.rule,1))
        pieces.append(_path('M 1260 510 L 1350 430 L 1325 530 L 1420 440 L 1380 585',t.accent,9))
    elif t.name=='tropical':
        for r in (82,150,224,306):
            pieces.append(_circle(1430,496,r,stroke=t.rule,sw=2))
        pieces.append(_path('M 1372 478 C 1470 376 1560 476 1495 552 C 1405 660 1306 560 1370 505',t.accent,10))
        pieces.append(_circle(1429,494,16,fill=t.secondary))
    elif t.name=='flood':
        for i in range(8):
            y=295+i*54
            pieces.append(_path(f'M 1250 {y} C 1340 {y-28} 1410 {y+31} 1510 {y}',t.secondary,2,opacity=.65))
        pieces.append(_text(1390,770,'HYDROGRAPH / RECORD',17,t.muted,'bold',anchor='middle',spacing=2))
    elif t.name=='temperature':
        for x in range(1290,1535,43):
            pieces.append(_line(x,320,x,715,t.rule,1))
        for h in range(5):
            pieces.append(_rect(1300+h*46,555-h*58,27,185+h*58,t.secondary if h%2 else t.accent))
    elif t.name=='drought':
        for i in range(9):
            pieces.append(_path(f'M {1210+i*35} 685 L {1285+i*27} 570 L {1230+i*30} 478',t.rule,3))
        for y in range(380,760,78):
            pieces.append(_path(f'M 1190 {y} C 1270 {y-28} 1380 {y+30} 1540 {y}',t.secondary,2))
    elif t.name=='wildfire_weather':
        for k in range(7):
            x=1260+k*46
            pieces.append(_path(f'M {x} 724 C {x-65} 610 {x+20} 512 {x-17} 400',t.secondary if k%2 else t.accent,3,opacity=.65))
        pieces.append(_line(1200,777,1545,777,t.accent,6))
    elif t.name=='unusual':
        for i in range(14):
            pieces.append(_line(1190,310+i*29,1530,310+i*29,t.accent if i%4==0 else t.rule,2))
        for cx,cy in ((1315,440),(1430,600)):
            pieces.append(_circle(cx,cy,63,stroke=t.secondary,sw=4))
    else:
        for y in range(340,745,48):
            pieces.append(_line(1220,y,1535,y,t.rule,1))
    return pieces


def _header(item,t,spec,typ):
    day=date.fromisoformat(item['event_date'])
    dateline=f'{day:%B} {day.day}, {day.year}'
    title=str(spec.get('title','Weather history'))
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">',
       f'<title>{_s(title)}</title>',f'<desc>{_s(item["alt"])}</desc>',
       _rect(0,0,W,H,t.paper),
       _rect(0,0,19,H,t.accent),
       _rect(1160,195,440,605,t.faint),
       # Vintage newspaper-type masthead, deliberately small and consistent.
       _text(73,89,'OTD',44,t.ink,'bold',family='serif'),
       _text(177,89,'wx',44,t.accent,'bold',family='serif'),
       _line(72,118,1535,118,t.ink,2),
       _text(74,151,'THE WEATHER ARCHIVE',15,t.muted,'bold',spacing=2.5),
       _text(1535,81,dateline,25,t.ink,'bold',anchor='end'),
       _text(1535,108,t.label,14,t.accent,'bold',anchor='end',spacing=2),
       _line(73,821,1535,821,t.rule,2),
       _text(74,851,'OTDwx  /  SOURCE-LED WEATHER HISTORY',17,t.muted,'bold',spacing=1),
       _text(1535,851,'SOURCE: '+str(item['source_name']).upper(),17,t.muted,anchor='end')]
    p+=_ornament(t)
    return p


def _headline(p,t,spec,typ):
    # Offset masthead line and loose large typography counter the rigid-card aesthetic.
    p.append(_rect(74,185,60,5,t.accent))
    kicker=spec.get('kicker') or {'bar_comparison':'THE RECORD','big_number':'BY THE NUMBERS',
      'contrast':'THE CONTRAST','morning_timeline':'EVENT SEQUENCE',
      'warning_timeline':'WARNING CHRONOLOGY','conceptual_schematic':'ATMOSPHERIC SETUP',
      'track_map':'DOCUMENTED PATH','point_map':'OBSERVED LOCATIONS'}[typ]
    p.append(_text(74,215,str(kicker).upper(),18,t.accent,'bold',spacing=2))
    _stack(p,74,276,spec.get('title','Weather history'),32,58,64,t,limit=2)
    if spec.get('subtitle'):
        _stack(p,76,399,spec['subtitle'],68,24,30,t,family='sans',weight='normal',color=t.muted,limit=2)


def _comparison(item,t,s,p):
    rows=s.get('rows',[])
    if len(rows)!=2 or any(not isinstance(r,dict) or type(r.get('value')) not in (float,int) or
            not math.isfinite(r['value']) or r['value']<0 for r in rows):
        raise ValueError('bar_comparison needs two nonnegative finite measured values')
    # Magazine layout: the featured value is huge, with two proportional strips
    # underneath. Unlike a generic dashboard, it adapts the negative space.
    _headline(p,t,s,'bar_comparison')
    main=rows[0]['value'];previous=rows[1]['value'];unit=str(s.get('unit',''))
    value_label=f'{main:g}{unit}' if unit in ('"','°','%') else f'{main:g} {unit}'.strip()
    p.append(_text(78,548,value_label,148,t.ink,'bold',family='serif'))
    p.append(_text(79,583,str(rows[0]['label']).upper()+'  /  FEATURED PERIOD',17,t.muted,'bold',spacing=2))
    p.append(_text(79,626,(s.get('comparison_label') or 'COMPARATIVE OBSERVATIONS').upper(),16,t.accent,'bold',spacing=2))
    peak=max(main,previous,1)
    for i,r in enumerate(rows):
        y=675+i*58
        p.append(_text(79,y+12,str(r['label']),25,t.ink,'bold'))
        p.append(_rect(280,y-10,690,19,t.rule))
        p.append(_rect(280,y-10,690*r['value']/peak,19,t.accent if i==0 else t.secondary))
        p.append(_text(996,y+12,(f'{r["value"]:g}{unit}' if unit in ('"','°','%') else f'{r["value"]:g} {unit}').strip(),28,t.ink,'bold',family='serif'))
    if s.get('footnote'):
        _stack(p,1189,650,s['footnote'],22,26,36,t,weight='normal',family='sans',color=t.ink,limit=4)


def _number(item,t,s,p):
    _headline(p,t,s,'big_number')
    p.append(_text(76,660,s.get('hero',''),178,t.accent,'bold',family='serif'))
    _stack(p,78,718,s.get('hero_label',''),53,25,31,t,weight='bold',family='sans',limit=2)
    details=s.get('detail_lines',[])
    for i,d in enumerate(details[:3]):
        _stack(p,1187,558+i*72,d,25,23,27,t,weight='normal',family='sans',limit=2)


def _contrast(item,t,s,p):
    _headline(p,t,s,'contrast')
    p.append(_rect(73,472,1120,283,t.faint))
    for i,key in enumerate(('left','right')):
        content=s.get(key,{})
        x=95+i*565
        p.append(_rect(x,493,60,8,t.accent if i==0 else t.secondary))
        p.append(_text(x,540,content.get('name',''),24,t.muted,'bold'))
        p.append(_text(x,655,content.get('value',''),96,t.ink,'bold',family='serif'))
        _stack(p,x,708,content.get('note',''),31,20,26,t,weight='normal',family='sans',limit=2)
    if s.get('footnote'): _stack(p,1200,680,s['footnote'],22,20,26,t,weight='normal',family='sans',limit=4)


def _timeline(item,t,s,p,typ):
    _headline(p,t,s,typ)
    p.append(_text(77,539,s.get('hero',''),103,t.accent,'bold',family='serif'))
    _stack(p,80,589,s.get('hero_label',''),62,24,29,t,weight='normal',family='sans',color=t.muted)
    p.append(_line(110,675,1116,675,t.rule,10))
    for idx,x in enumerate((110,1116)):
        p.append(_circle(x,675,14,t.accent if idx==0 else t.secondary,stroke=t.paper,sw=3))
    p.append(_text(110,652,s.get('start',''),25,t.ink,'bold'))
    p.append(_text(1116,652,s.get('end',''),25,t.ink,'bold',anchor='end'))
    for i,detail in enumerate(s.get('detail_lines',[])[:4]):
        _stack(p,1186,480+i*77,detail,26,20,25,t,weight='normal',family='sans',limit=2)


def _schematic(item,t,s,p):
    _headline(p,t,s,'conceptual_schematic')
    p.append(_rect(80,471,1070,255,t.faint))
    p.append(_rect(80,472,1070,66,t.secondary))
    p.append(_text(611,520,s.get('upper','UPPER LAYER'),29,t.ink,'bold',anchor='middle'))
    p.append(_line(80,542,1150,542,t.accent,5))
    p.append(_text(610,615,s.get('middle','NEAR-SURFACE LAYER'),31,t.ink,'bold',anchor='middle'))
    p.append(_text(610,678,s.get('lower',''),21,t.muted,anchor='middle'))
    foot=s.get('footnote','CONCEPTUAL SCHEMATIC — NOT AN OBSERVATION')
    _stack(p,1191,670,foot,22,21,28,t,color=t.muted,weight='normal',family='sans',limit=3)


def _coords(value):
    if not isinstance(value,(tuple,list)) or len(value)!=2:raise ValueError('Map coordinates must be [longitude, latitude]')
    lon,lat=map(float,value)
    if not (math.isfinite(lon) and math.isfinite(lat) and -180<=lon<=180 and -90<=lat<=90):
        raise ValueError('Map coordinates outside geographic limits')
    return lon,lat


def _map(item,t,s,p,typ):
    bounds=s.get('bounds')
    if not isinstance(bounds,list) or len(bounds)!=4:raise ValueError('Maps require bounds [W,S,E,N]')
    west,south=_coords(bounds[:2]);east,north=_coords(bounds[2:])
    if east<=west or north<=south or east-west>100 or north-south>70:
        raise ValueError('Map bounds invalid or too broad')
    if not s.get('data_source_url') or urlparse(str(s['data_source_url'])).scheme!='https':
        raise ValueError('Map source-backed observations require an HTTPS data_source_url')
    if s.get('geography') and not s.get('geography_source_url'):
        raise ValueError('Map geography overlays require a geography_source_url')
    _headline(p,t,s,typ)
    p.append(_rect(76,433,1446,335,t.faint))
    xlo,xhi,ylo,yhi=85,1512,440,759
    def loc(coords):
        lon,lat=_coords(coords)
        if not (west<=lon<=east and south<=lat<=north):raise ValueError('Map feature coordinate outside bounds')
        return xlo+(xhi-xlo)*(lon-west)/(east-west), yhi-(yhi-ylo)*(lat-south)/(north-south)
    for i in range(1,8):
        x=xlo+i*(xhi-xlo)/8;p.append(_line(x,ylo,x,yhi,t.rule,1))
    for i in range(1,4):
        y=ylo+i*(yhi-ylo)/4;p.append(_line(xlo,y,xhi,y,t.rule,1))
    for f in s.get('geography',[]):
        if f.get('type') not in ('LineString','Polygon'):raise ValueError('Geography accepts LineString/Polygon only')
        seq=f['coordinates'] if f['type']=='LineString' else f['coordinates'][0]
        if not 2<=len(seq)<=10000:raise ValueError('Invalid geographic feature length')
        points=' '.join(f'{x:.2f},{y:.2f}' for x,y in map(loc,seq))
        p.append(f'<polyline points="{points}" fill="none" stroke="{t.muted}" stroke-width="2"/>')
    if typ=='track_map':
        pts=s.get('track',[])
        if not 2<=len(pts)<=1000:raise ValueError('Track map needs 2–1000 observed points')
        quality=s.get('track_quality')
        if quality not in ('surveyed','best_track','approximate'):
            raise ValueError('Track quality must be surveyed, best_track or approximate')
        pos=list(map(loc,pts))
        p.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pos)}" fill="none" stroke="{t.accent}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"'+(' stroke-dasharray="18 12"' if quality=='approximate' else '')+'/>')
        for x,y in (pos[0],pos[-1]):p.append(_circle(x,y,10,t.paper,stroke=t.accent,sw=5))
        p.append(_text(94,790,'SURVEYED PATH' if quality=='surveyed' else 'BEST TRACK' if quality=='best_track' else 'APPROXIMATE PATH — NOT A SURVEY',17,t.accent,'bold',spacing=2))
    else:
        pts=s.get('points',[])
        if not 1<=len(pts)<=40:raise ValueError('Point map needs 1–40 observed locations')
        for pt in pts:
            x,y=loc(pt['coordinates'])
            label=str(pt['label'])
            if len(label)>30:raise ValueError('Point label too long')
            p.append(_circle(x,y,10,t.accent,stroke=t.paper,sw=3))
            p.append(_text(x+15,y-14,label,20,t.ink,'bold'))
    p.append(_text(1511,790,s.get('map_note','GEOGRAPHIC GRID • NOT DISTANCE-PRESERVING'),15,t.muted,anchor='end'))


def render_themed(item):
    """Render vetted *input* facts. Rendering does not independently verify truth."""
    if item.get('type') not in TYPES:raise ValueError('Unsupported graphic type')
    if not isinstance(item.get('graphic_spec'),dict):raise ValueError('graphic_spec must be an object')
    if not item.get('source_name') or not item.get('alt'):raise ValueError('source_name and alt required')
    date.fromisoformat(item['event_date'])
    t=_theme(item);s=item['graphic_spec'];typ=item['type']
    p=_header(item,t,s,typ)
    if typ=='bar_comparison':_comparison(item,t,s,p)
    elif typ=='big_number':_number(item,t,s,p)
    elif typ=='contrast':_contrast(item,t,s,p)
    elif typ in ('morning_timeline','warning_timeline'):_timeline(item,t,s,p,typ)
    elif typ=='conceptual_schematic':_schematic(item,t,s,p)
    else:_map(item,t,s,p,typ)
    p.append('</svg>')
    return '\n'.join(p)+'\n'


def validate_themed(item):
    try:render_themed(item)
    except (ValueError,KeyError,TypeError,OverflowError) as exc:return [str(exc)]
    return []