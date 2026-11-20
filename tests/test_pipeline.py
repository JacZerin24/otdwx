import gzip
from datetime import date
import unittest
from otdwx.pipeline import (
    ncei_files, hurdat_files, parse_ncei, parse_hurdat,
    rated, plan_days, candidates_by_day
)

class Phase2Tests(unittest.TestCase):
    def test_revisions(self):
        data = ("StormEvents_details-ftp_v1.0_d2024_c20260323.csv.gz "
                "StormEvents_details-ftp_v1.0_d2024_c20261119.csv.gz")
        self.assertTrue(ncei_files(data,2024,2024)[2024].endswith("c20261119.csv.gz"))

    def test_nhc_index(self):
        index = ("hurdat2-1851-2024-04042025.txt "
                 "hurdat2-1851-2025-09302026.txt "
                 "hurdat2-nepac-1949-2025-09292026.txt")
        self.assertEqual(len(hurdat_files(index)),2)

    def test_ncei_factual_fields_only(self):
        data = ("EVENT_ID,BEGIN_YEARMONTH,BEGIN_DAY,EVENT_TYPE,STATE,BEGIN_LOCATION,"
                "DEATHS_DIRECT,INJURIES_DIRECT,TOR_F_SCALE,EVENT_NARRATIVE\n"
                "12345,199804,8,Tornado,ALABAMA,Concord,1,12,F4,Test account\n")
        rows = parse_ncei(gzip.compress(data.encode()),"https://example.org/test.gz")
        self.assertEqual(rows[0]["event_date"],"1998-04-08")
        self.assertEqual(rows[0]["region"],"Southeast")
        self.assertEqual(rows[0]["status"],"researching")
        self.assertEqual(rows[0]["source_record_id"],"12345")

    def test_hurdat_not_mistaken_for_impact_data(self):
        txt = ("AL012005, KATRINA, 3,\n"
               "20050828, 1800, , HU, 26.0N, 87.0W, 150, 902,\n"
               "20050829, 1110, L, HU, 29.0N, 89.0W, 110, 920,\n"
               "20050829, 1800, , HU, 30.0N, 89.5W, 80, 950,\n")
        rows=parse_hurdat(txt,"https://example.org/hurdat.txt","atlantic")
        self.assertEqual(len(rows),2)
        self.assertTrue(all(x["status"]=="researching" for x in rows))
        self.assertTrue(all(x["evidence_status"].startswith("track_only") for x in rows))

    def example(self,ident="x",when="2000-02-29",kind="winter",reg="Midwest",src="ncei-storm-events"):
        return {"event_id":ident,"event_date":when,"weather_type":kind,
                "region":reg,"source_id":src,"base_score":80}

    def test_repeating_event_disallowed(self):
        c=self.example()
        self.assertLess(rated(c,[c])[0],-1000)

    def test_repeated_source_region_hazard_are_penalized(self):
        c=self.example()
        prev=self.example("other")
        self.assertLess(rated(c,[prev])[0],80)

    def test_leap_day(self):
        c=self.example()
        self.assertEqual(plan_days([c],[],date(2028,2,29),1)[0]["event_id"],"x")

    def test_no_fabricated_candidates(self):
        self.assertEqual(plan_days([],[],date(2026,11,20),1)[0]["status"],"no_candidate")

    def test_per_day_region_cap(self):
        events=[self.example(str(i),"1999-01-01","tornado","Midwest") for i in range(25)]
        self.assertLessEqual(len(candidates_by_day(events)),3)

if __name__=="__main__":
    unittest.main()
