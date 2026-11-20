"""OTDwx Phase 2: NCEI and NHC historical research candidates (never posts)."""
from __future__ import annotations

import argparse
import csv
from datetime import date, datetime, timedelta
import gzip
from io import BytesIO
import json
import math
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

NCEI = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
NHC = "https://www.nhc.noaa.gov/data/hurdat/"
KINDS = {
 "TORNADO":"tornado", "THUNDERSTORM WIND":"severe_storm", "HAIL":"severe_storm",
 "HIGH WIND":"severe_storm","STRONG WIND":"severe_storm","FLASH FLOOD":"flood",
 "FLOOD":"flood","COASTAL FLOOD":"flood","STORM SURGE/TIDE":"flood",
 "HEAVY SNOW":"winter","BLIZZARD":"winter","ICE STORM":"winter",
 "WINTER STORM":"winter","WINTER WEATHER":"winter","LAKE-EFFECT SNOW":"winter",
 "EXCESSIVE HEAT":"temperature","HEAT":"temperature",
 "EXTREME COLD/WIND CHILL":"temperature","COLD/WIND CHILL":"temperature",
 "DROUGHT":"drought","DENSE FOG":"unusual","DUST STORM":"unusual",
 "WILDFIRE":"wildfire_weather","HURRICANE (TYPHOON)":"tropical",
 "TROPICAL STORM":"tropical"
}
REGIONS = {
 "ALABAMA":"Southeast","FLORIDA":"Southeast","GEORGIA":"Southeast",
 "NORTH CAROLINA":"Southeast","SOUTH CAROLINA":"Southeast",
 "MISSISSIPPI":"Gulf Coast","LOUISIANA":"Gulf Coast",
 "TEXAS":"South Central","OKLAHOMA":"South Central","ARKANSAS":"South Central",
 "OHIO":"Ohio Valley","KENTUCKY":"Ohio Valley","TENNESSEE":"Ohio Valley",
 "WEST VIRGINIA":"Appalachia","MICHIGAN":"Great Lakes","WISCONSIN":"Great Lakes",
 "ILLINOIS":"Midwest","INDIANA":"Midwest","MISSOURI":"Midwest",
 "IOWA":"Upper Midwest","MINNESOTA":"Upper Midwest",
 "KANSAS":"Great Plains","NEBRASKA":"Great Plains",
 "NORTH DAKOTA":"Great Plains","SOUTH DAKOTA":"Great Plains",
 "IDAHO":"Northern Rockies","MONTANA":"Northern Rockies",
 "WYOMING":"Northern Rockies","UTAH":"Rockies","COLORADO":"Rockies",
 "ARIZONA":"Southwest","NEW MEXICO":"Southwest","NEVADA":"Great Basin",
 "CALIFORNIA":"West Coast","OREGON":"West Coast","WASHINGTON":"West Coast",
 "MAINE":"Northeast","VERMONT":"Northeast","NEW HAMPSHIRE":"Northeast",
 "MASSACHUSETTS":"Northeast","CONNECTICUT":"Northeast","RHODE ISLAND":"Northeast",
 "NEW YORK":"Northeast","PENNSYLVANIA":"Northeast","NEW JERSEY":"Northeast",
 "VIRGINIA":"Mid-Atlantic","MARYLAND":"Mid-Atlantic","DELAWARE":"Mid-Atlantic",
 "ALASKA":"Alaska","HAWAII":"Hawaii","PUERTO RICO":"Caribbean","GUAM":"Pacific Islands"
}

def fetch(url: str) -> bytes:
    if not url.startswith("https://"): raise ValueError("HTTPS required")
    req=Request(url,headers={"User-Agent":"OTDwx historical research/0.2"})
    with urlopen(req,timeout=90) as r: return r.read()

def ncei_files(index: str, first: int, last: int) -> dict[int,str]:
    found={}
    for name,year,version in re.findall(
        r"(StormEvents_details-ftp_v1\.0_d(\d{4})_c(\d{8})\.csv\.gz)",index):
        year=int(year)
        if first<=year<=last and (year not in found or version>found[year][0]):
            found[year]=(version,urljoin(NCEI,name))
    return {year:found[year][1] for year in sorted(found)}

def hurdat_files(index: str) -> dict[str,str]:
    names=set(re.findall(r"hurdat2-[A-Za-z0-9-]+\.txt",index))
    patterns={
       "atlantic":r"hurdat2-(?:atl-)?1851-(\d{4})-(\d+)\.txt",
       "pacific":r"hurdat2-(?:nepac|nencpac)-1949-(\d{4})-(\d+)\.txt"
    }
    result={}
    for basin,pattern in patterns.items():
        possibilities=[]
        for name in names:
            m=re.fullmatch(pattern,name)
            if m: possibilities.append(((int(m[1]),m[2]),name))
        if possibilities:result[basin]=urljoin(NHC,max(possibilities)[1])
    return result

def nonnegative_int(raw) -> int:
    try:return max(0,int(float(str(raw or 0).replace(",",""))))
    except (ValueError,OverflowError):return 0

def storm_date(row:dict) -> str | None:
    ym=str(row.get("BEGIN_YEARMONTH","")).strip()
    d=str(row.get("BEGIN_DAY","")).strip()
    if re.fullmatch(r"\d{6}",ym) and d.isdigit():
        try:return date(int(ym[:4]),int(ym[4:]),int(d)).isoformat()
        except ValueError:return None
    for fmt in ("%d-%b-%y %H:%M:%S","%d-%b-%Y %H:%M:%S","%m/%d/%Y %H:%M:%S"):
        try:return datetime.strptime(str(row.get("BEGIN_DATE_TIME","")),fmt).date().isoformat()
        except ValueError:pass
    return None

def parse_ncei(gzip_bytes:bytes, source_url:str, minimum_score:float=15) -> list[dict]:
    out=[]
    with gzip.open(BytesIO(gzip_bytes),"rt",encoding="utf-8-sig",errors="replace",newline="") as f:
        for row in csv.DictReader(f):
            hazard=str(row.get("EVENT_TYPE","")).strip().upper()
            day=storm_date(row)
            ident=str(row.get("EVENT_ID","")).strip()
            if hazard not in KINDS or not day or not ident.isdigit():continue
            deaths=nonnegative_int(row.get("DEATHS_DIRECT"))+nonnegative_int(row.get("DEATHS_INDIRECT"))
            injured=nonnegative_int(row.get("INJURIES_DIRECT"))+nonnegative_int(row.get("INJURIES_INDIRECT"))
            narrative=" ".join((row.get("EVENT_NARRATIVE") or row.get("EPISODE_NARRATIVE") or "").split())[:300]
            rating=str(row.get("TOR_F_SCALE") or "").upper().strip()
            bonus=14 if rating in ("F4","EF4","F5","EF5") else (7 if rating in ("F3","EF3") else 0)
            score=9+min(35,12*math.log1p(deaths))+min(20,3*math.log1p(injured))+bonus+min(10,len(narrative)//30)
            if score<minimum_score:continue
            state=str(row.get("STATE") or "").upper().strip()
            place=str(row.get("BEGIN_LOCATION") or row.get("CZ_NAME") or "").strip()
            location=", ".join(x for x in (place,state.title()) if x)
            out.append({
               "event_id":f"ncei-{ident}","event_date":day,
               "title":f"{hazard.title()} — {location or 'United States'}",
               "weather_type":KINDS[hazard],"region":REGIONS.get(state,state.title()),
               "location":location,"country":"USA","source_id":"ncei-storm-events",
               "source_publisher":"NOAA NCEI Storm Events","source_url":source_url,
               "source_record_id":ident,"summary":narrative,
               "source_facts":{"deaths_reported":deaths,"injuries_reported":injured,
                               "event_type":hazard,"tornado_rating":rating},
               "base_score":round(score,2),"evidence_status":"source_record_only",
               "status":"researching",
               "research_note":"Check exact dates, impacts, individual-event vs outbreak totals, source updates, and media rights."
            })
    return out

def parse_hurdat(content:str, source_url:str, basin:str) -> list[dict]:
    """Best tracks show positions/intensity, not human impacts."""
    result=[];identifier="";name="";records=[]
    def flush():
        if not identifier:return
        landfalls=[(r,"landfall_marker") for r in records if len(r)>=8 and r[2]=="L"]
        eligible=[r for r in records if len(r)>=8 and re.fullmatch(r"-?\d+",r[6])]
        if eligible:
            peak=max(eligible,key=lambda r:int(r[6]))
            if int(peak[6])>=100 and not any(x[0]==peak[0] for x,_ in landfalls):
                landfalls.append((peak,"peak_wind"))
        for r,reason in landfalls:
            try:
                day=date(int(r[0][:4]),int(r[0][4:6]),int(r[0][6:8]))
                wind=int(r[6])
            except (ValueError,IndexError):continue
            if wind<0 or r[3] not in ("HU","TS","TD","SS","SD"):continue
            title=name.title() if name and name!="UNNAMED" else identifier
            position=f"{r[4]} {r[5]}"
            result.append({
               "event_id":f"nhc-{identifier.lower()}-{r[0]}-{reason}",
               "event_date":day.isoformat(),
               "title":f"{title} — {reason.replace('_',' ')}",
               "weather_type":"tropical","region":"Atlantic basin" if basin=="atlantic" else "Pacific basin",
               "location":position+" (geography unverified)","country":"Unconfirmed",
               "source_id":f"nhc-hurdat-{basin}","source_publisher":"NOAA National Hurricane Center",
               "source_url":source_url,"source_record_id":identifier,
               "summary":f"Best track: {r[1]} UTC, {position}, maximum wind {wind} kt.",
               "source_facts":{"wind_kt":wind,"record_marker":r[2],"storm_status":r[3]},
               "base_score":round(14+min(30,wind/4)+(12 if reason=="landfall_marker" else 2),2),
               "evidence_status":"track_only_needs_impact_verification","status":"researching",
               "research_note":"Track point is not evidence of damages. Confirm exact location, local date, impact details."
            })
    for line in content.splitlines():
        values=[x.strip() for x in line.split(",")]
        if values and re.fullmatch(r"(?:AL|EP|CP)\d{6}",values[0]):
            flush();identifier=values[0];name=values[1] if len(values)>1 else "";records=[]
        elif identifier and len(values)>=8 and re.fullmatch(r"\d{8}",values[0]):
            records.append(values)
    flush()
    return result

def candidates_by_day(data:list[dict],limit:int=14) -> list[dict]:
    groups={}
    for item in data: groups.setdefault(item["event_date"][5:],[]).append(item)
    selected=[]
    for key,group in sorted(groups.items()):
        counts={};picked=0
        for c in sorted(group,key=lambda x:(-x["base_score"],x["event_id"])):
            if picked>=limit:break
            checks=[("region",c["region"],3),("weather",c["weather_type"],6),
                    ("source",c["source_id"],10)]
            if any(counts.get((kind,val),0)>=cap for kind,val,cap in checks):continue
            selected.append(c);picked+=1
            for kind,val,_ in checks:counts[(kind,val)]=counts.get((kind,val),0)+1
    return selected

def rated(candidate:dict,history:list[dict]) -> tuple[float,list[str]]:
    if any(candidate["event_id"]==x.get("event_id") for x in history):
        return -9999,["already_used"]
    score=float(candidate["base_score"]);notes=[]
    for i,old in enumerate(reversed(history[-14:]),1):
        for key,cost in (("region",24),("weather_type",16),("source_id",12)):
            if candidate.get(key) and candidate.get(key)==old.get(key):
                amt=round(cost/(i**0.75),1)
                score-=amt;notes.append(f"{key} -{amt}")
    if int(candidate["event_date"][:4])<1950:score+=3
    return round(score,2),notes

def plan_days(candidates:list[dict],history:list[dict],start:date,days:int) -> list[dict]:
    planned=[];lookup={c["event_id"]:c for c in candidates}
    for offset in range(days):
        day=start+timedelta(days=offset)
        pool=[]
        used=history+[lookup[p["event_id"]] for p in planned if p["event_id"]]
        for c in candidates:
            if c["event_date"][5:]!=day.strftime("%m-%d"):continue
            score,notes=rated(c,used)
            if score>-100:pool.append((score,c,notes))
        pool.sort(key=lambda row:(-row[0],row[1]["event_id"]))
        planned.append({
          "planned_date":day.isoformat(),"event_id":pool[0][1]["event_id"] if pool else "",
          "selection_score":pool[0][0] if pool else None,
          "alternatives":[x[1]["event_id"] for x in pool[1:4]],
          "reason_codes":pool[0][2] if pool else [],
          "status":"researching" if pool else "no_candidate"
        })
    return planned

def build(first:int,last:int,start:date,days:int) -> dict:
    from collections import Counter
    errors=[];source_stats={};raw=[]
    years=ncei_files(fetch(NCEI).decode("utf-8","replace"),first,last)
    if not years:raise RuntimeError("No matching NCEI archive years; refusing overwrite")
    for year,url in years.items():
        try:
            found=parse_ncei(fetch(url),url);raw+=found;source_stats[f"ncei_{year}"]=len(found)
            print(f"Processed NCEI {year}: {len(found)} candidates",flush=True)
        except Exception as exc:
            errors.append(f"NCEI {year}: {exc}")
            print(errors[-1],flush=True)
    try:
        hfiles=hurdat_files(fetch(NHC).decode("utf-8","replace"))
        if not hfiles:errors.append("NHC index had no matching HURDAT2 filename")
        for basin,url in hfiles.items():
            try:
                found=parse_hurdat(fetch(url).decode("utf-8","replace"),url,basin)
                raw+=found;source_stats[f"nhc_{basin}"]=len(found)
            except Exception as exc:errors.append(f"NHC {basin}: {exc}")
    except Exception as exc:errors.append(f"NHC index: {exc}")
    if not raw:raise RuntimeError("No records parsed from archives; preserved previous catalog")
    unique={c["event_id"]:c for c in raw}
    selected=candidates_by_day(list(unique.values()))
    try:published=json.loads(Path("data/publishing_log.json").read_text(encoding="utf-8"))
    except FileNotFoundError:published=[]
    plan=plan_days(selected,published,start,days)
    covered={c["event_date"][5:] for c in selected}
    all_days={(date(2024,1,1)+timedelta(days=i)).strftime("%m-%d") for i in range(366)}
    meta={
       "generated_at":datetime.now(ZoneInfo("America/Chicago")).isoformat(),
       "years":f"{first}-{last}","raw_unique_records":len(unique),
       "total_candidates":len(selected),"anniversary_days_covered":len(covered),
       "anniversary_days_uncovered":sorted(all_days-covered),
       "plan_days":len(plan),"unfilled_plan_days":sum(not p["event_id"] for p in plan),
       "source_counts":source_stats,
       "source_families":dict(Counter(c["source_id"] for c in selected)),
       "warnings":errors,
       "notice":"Unverified research leads — human fact check required; not publishable copy."
    }
    return {"metadata":meta,"candidates":selected,"plan":plan}

def export_csv(payload:dict,folder:Path) -> None:
    folder.mkdir(parents=True,exist_ok=True)
    catalog=payload["candidates"];lookup={c["event_id"]:c for c in catalog}
    def write(name,columns,records):
        with (folder/name).open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=columns)
            writer.writeheader();writer.writerows(records)
    rows=[{
      "Event ID":c["event_id"],"Event Date":c["event_date"],"Working Title":c["title"],
      "Location":c["location"],"Region":c["region"],"Weather Type":c["weather_type"],
      "Source URL":c["source_url"],"Evidence Status":c["evidence_status"],
      "Source Score":c["base_score"],"Source Narrative":c["summary"],
      "Review Status":"researching"
    } for c in catalog]
    cols=["Event ID","Event Date","Working Title","Location","Region","Weather Type",
          "Source URL","Evidence Status","Source Score","Source Narrative","Review Status"]
    write("discovery_feed.csv",cols,rows)
    plans=[]
    for p in payload["plan"]:
        c=lookup.get(p["event_id"],{})
        plans.append({
          "Planned Date":p["planned_date"],"Event ID":p["event_id"],
          "Title":c.get("title","RESEARCH GAP"),"Region":c.get("region",""),
          "Weather Type":c.get("weather_type",""),"Source URL":c.get("source_url",""),
          "Score":p["selection_score"] if p["selection_score"] is not None else "",
          "Alternatives":", ".join(p["alternatives"]),"Status":p["status"]
        })
    write("daily_suggestions.csv",["Planned Date","Event ID","Title","Region","Weather Type",
                                   "Source URL","Score","Alternatives","Status"],plans)

def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start-year",type=int,default=1996)
    p.add_argument("--end-year",type=int,default=2025)
    p.add_argument("--start-date",default="")
    p.add_argument("--days",type=int,default=60)
    args=p.parse_args(argv)
    if args.start_year>args.end_year or args.days<1 or args.days>366:p.error("Invalid range or days")
    start=date.fromisoformat(args.start_date) if args.start_date else datetime.now(ZoneInfo("America/Chicago")).date()
    result=build(args.start_year,args.end_year,start,args.days)
    path=Path("data/discovery_candidates.json")
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    export_csv(result,Path("exports"))
    print(json.dumps(result["metadata"],indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
