"""Discover and stage original weather archive media, without claiming reuse rights.

Examples:
  python -m otdwx.archive_ingest discover --page https://www.weather.gov/ilm/2006-Nov-16tornado
  python -m otdwx.archive_ingest fetch --url <verified-archive-asset-url> \
      --page https://www.weather.gov/ilm/2006-Nov-16tornado \
      --output /private/otdwx/source-assets/survey.png

Internet access is required at runtime; no simulated radar, track or photography.
Download metadata always starts rights_status=researching, approval=pending.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import socket
from urllib.parse import urljoin,urlparse
from urllib.request import Request,build_opener,HTTPRedirectHandler


MAX_DOWNLOAD=20_000_000
GOOD_EXT={".png",".jpeg",".jpg",".gif",".webp",".pdf",".geojson",".json"}
USER_AGENT="OTDwx-Research/1.0 (+source-review; noncommercial-download)"


def _public_https(value: str):
    p=urlparse(value)
    if p.scheme!="https" or not p.netloc or p.username or p.password:
        raise ValueError("Only explicit public HTTPS archive URLs are accepted")
    host=p.hostname
    if host in ("localhost","127.0.0.1") or host.endswith(".local"):
        raise ValueError("Loopback/private host prohibited")
    try:
        addresses=socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError("Unable to resolve archival host") from exc
    for addr in addresses:
        try:ip=ipaddress.ip_address(addr[4][0])
        except ValueError:raise ValueError("Invalid resolved address")
        if not ip.is_global:
            raise ValueError("Archive host resolves to a non-public IP")
    return p


class _PublicRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        _public_https(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)


def _open(request,timeout):
    return build_opener(_PublicRedirect()).open(request,timeout=timeout)


class EvidenceLinkParser(HTMLParser):
    def __init__(self,base):
        super().__init__()
        self.base=base
        self.items=[]
    def handle_starttag(self,tag,attrs):
        attr=dict(attrs)
        if tag not in ("a","img","video","source"):
            return
        value=attr.get("href") if tag=="a" else attr.get("src")
        if not value:
            return
        url=urljoin(self.base,value)
        suffix=Path(urlparse(url).path).suffix.lower()
        if suffix not in GOOD_EXT:
            return
        title=(attr.get("alt") or attr.get("title") or attr.get("aria-label") or "")[:160]
        self.items.append({"tag":tag,"asset_url":url,"caption_hint":title})


def discover(page: str):
    _public_https(page)
    with _open(Request(page,headers={"User-Agent":USER_AGENT}),timeout=30) as r:
        if r.geturl()!=page:_public_https(r.geturl())
        raw=r.read(2_000_000+1)
    if len(raw)>2_000_000:raise ValueError("Large HTML archive page: manual review needed")
    p=EvidenceLinkParser(page)
    p.feed(raw.decode("utf-8",errors="replace"))
    unique={}
    for a in p.items:
        if a["asset_url"] not in unique:unique[a["asset_url"]]=a
    return list(unique.values())


def fetch(url: str, page: str, output: Path):
    _public_https(url);_public_https(page)
    output=Path(output)
    if output.suffix.lower() not in GOOD_EXT:
        raise ValueError("Only image, PDF, and GeoJSON archive downloads are supported")
    if output.exists():raise FileExistsError(output)
    request=Request(url,headers={"User-Agent":USER_AGENT})
    with _open(request,timeout=40) as r:
        final=r.geturl()
        _public_https(final)
        raw=r.read(MAX_DOWNLOAD+1)
        mime=r.headers.get("Content-Type","").split(";")[0]
    if len(raw)>MAX_DOWNLOAD:raise ValueError("Archive file above 20MB; use dedicated ingestion")
    if output.suffix.lower()==".png" and not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Archive server did not provide a PNG")
    if output.suffix.lower() in (".jpg",".jpeg") and not raw.startswith(b"\xff\xd8\xff"):
        raise ValueError("Archive server did not provide a JPEG")
    if output.suffix.lower()==".gif" and not raw.startswith((b"GIF87a",b"GIF89a")):
        raise ValueError("Archive server did not provide a GIF")
    if output.suffix.lower()==".pdf" and not raw.startswith(b"%PDF"):
        raise ValueError("Archive server did not provide a PDF")
    if output.suffix.lower() in (".geojson",".json"):
        try:json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError,json.JSONDecodeError) as exc:
            raise ValueError("Not a valid UTF-8 JSON dataset") from exc
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(raw)
    meta={
        "source_page":page, "original_asset_url":url, "resolved_url":final,
        "file":str(output.name), "bytes":len(raw),
        "sha256":sha256(raw).hexdigest(),"mime_type":mime,
        "rights_status":"researching", "human_approval":"pending",
        "note":"Download and checksum verified, NOT copyright cleared or meteorologically reviewed."
    }
    output.with_name(output.name+".provenance.json").write_text(
        json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    return meta


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest="cmd",required=True)
    d=subs.add_parser("discover");d.add_argument("--page",required=True)
    f=subs.add_parser("fetch");f.add_argument("--page",required=True)
    f.add_argument("--url",required=True)
    f.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(argv)
    result=discover(args.page) if args.cmd=="discover" else fetch(args.url,args.page,args.output)
    print(json.dumps(result,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
