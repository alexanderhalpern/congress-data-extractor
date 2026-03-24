TRANSCRIPT_CHARS = 30000
API_CHARS = 4000

PROMPT = """You are a research assistant extracting structured data from a congressional committee field hearing. You will receive structured JSON from the Congress.gov API followed optionally by extracted text from the hearing transcript, member roster, or witness list PDF.

First, set sufficient_data to true only if there is enough information to identify the host/chair, at least some witnesses, and basic hearing metadata. If only a bare stub is available with no host or witness info, set sufficient_data to false and explain briefly in missing_reason. If sufficient_data is false, you may leave hearing/witnesses/members as empty/null placeholders.

HEARINGDATA fields:
- hearingID: Committee_MMDDYYYY_CityStateAbbrev_H  e.g. Oversight_04232024_PlanoTX_H
- date: YYYY-MM-DD
- title: Exact hearing title from the document
- topic: 3-6 comma-separated theme keywords
- committee: Short committee name
- subcommitteee: 1 if subcommittee hearing, 0 if full committee
- subcomittee_name: Full subcommittee name or null
- chamber: H or S
- majparty: Majority party that congress — R or D
- congress: Congressional session number e.g. 118
- midterm: 1 if even-numbered year, 0 if odd
- location_city: City, town, or county of the hearing
- location_CD: Congressional district e.g. TX-4. DC-0 for Washington DC. List both if city spans two districts e.g. TX-4/TX-5
- location_type: Urban | Suburban | Rural | Rural-suburban mix | Suburban-urban mix
- host: Last name of the member chairing/hosting the hearing (title page or opening statements)
- host2: Last name of second host or null
- host_homeCD: 1 if host represents the hearing district/state, 0 if not
- open: 1 if open to the public, 0 if not (default 1 if unclear)
- num_witnesses: Total witness count
- num_MCs: Total members of Congress present (check opening statements, not just title page)
- D_present: Democrats present
- R_present: Republicans present
- chair_present: 1 if full committee chair present, 0 if not
- subcommitteechair_present: 1 if subcommittee chair present, 0 if not; null if not a subcommittee hearing
- ratio_present: null
- pdfname: hearingID + ".pdf"
- notes: Anything interesting about witnesses, members, or the hearing

WITNESSDATA fields (one entry per witness):
- hearingID: same as above
- witness_name: Full name
- witness_occupation: Their stated title or role
- witness_rep: Organization or entity they represent
- witness_type: academic | interest group | personal interest | business | federal government | state government | MC | nonprofit
- speaking_order: Order of opening statements (1, 2, 3...)
- agreement_chair: null
- notes: Anything interesting about this witness

MEMBERDATA fields (one entry per host; two entries if two hosts):
- hearingID: same as above
- host_name: Full name of the host/chair
- host_BioGuideID: From https://www.congress.gov/help/field-values/member-bioguide-ids — null if unknown
- host_party: R or D
- host_homeCD: 1 if host is from the hearing district/state, 0 if not
- CD_MC: Name of the MC representing the hearing's congressional district
- CD_MC_bioguideID: BioGuide ID for that MC — null if unknown
- CD_hostvoteshare: Host's vote share % in most recent election before hearing date — null if unknown
- CD_Dpresvoteshare: Democratic presidential vote share % in district in most recent presidential election before hearing — null if unknown
- host_vulnerable: Cook PVI — 0: not vulnerable, 1: under Likely own party, 2: under Lean own party, 3: toss-up or leaning opposing; null if unknown
- notes: null"""

OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["sufficient_data", "missing_reason", "hearing", "witnesses", "members"],
    "properties": {
        "sufficient_data": {"type": "boolean"},
        "missing_reason": {"type": ["string", "null"]},
        "hearing": {
            "type": "object",
            "additionalProperties": False,
            "required": ["hearingID","date","title","committee","subcommitteee","subcomittee_name","chamber","majparty","congress","midterm","location_city","location_CD","location_type","host","host2","host_homeCD","topic","open","num_witnesses","num_MCs","D_present","R_present","chair_present","subcommitteechair_present","ratio_present","pdfname","notes"],
            "properties": {
                "hearingID":                 {"type": "string"},
                "date":                      {"type": "string"},
                "title":                     {"type": "string"},
                "committee":                 {"type": "string"},
                "subcommitteee":             {"type": "integer"},
                "subcomittee_name":          {"type": ["string","null"]},
                "chamber":                   {"type": "string"},
                "majparty":                  {"type": "string"},
                "congress":                  {"type": "integer"},
                "midterm":                   {"type": "integer"},
                "location_city":             {"type": "string"},
                "location_CD":               {"type": "string"},
                "location_type":             {"type": "string"},
                "host":                      {"type": "string"},
                "host2":                     {"type": ["string","null"]},
                "host_homeCD":               {"type": ["integer","null"]},
                "topic":                     {"type": "string"},
                "open":                      {"type": "integer"},
                "num_witnesses":             {"type": "integer"},
                "num_MCs":                   {"type": "integer"},
                "D_present":                 {"type": "integer"},
                "R_present":                 {"type": "integer"},
                "chair_present":             {"type": "integer"},
                "subcommitteechair_present": {"type": ["integer","null"]},
                "ratio_present":             {"type": ["number","null"]},
                "pdfname":                   {"type": "string"},
                "notes":                     {"type": ["string","null"]},
            },
        },
        "witnesses": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["hearingID","witness_name","witness_occupation","witness_rep","witness_type","speaking_order","agreement_chair","notes"],
                "properties": {
                    "hearingID":          {"type": "string"},
                    "witness_name":       {"type": "string"},
                    "witness_occupation": {"type": "string"},
                    "witness_rep":        {"type": "string"},
                    "witness_type":       {"type": "string"},
                    "speaking_order":     {"type": "integer"},
                    "agreement_chair":    {"type": ["string","null"]},
                    "notes":              {"type": ["string","null"]},
                },
            },
        },
        "members": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["hearingID","host_name","host_BioGuideID","host_party","host_homeCD","CD_MC","CD_MC_bioguideID","CD_hostvoteshare","CD_Dpresvoteshare","host_vulnerable","notes"],
                "properties": {
                    "hearingID":         {"type": "string"},
                    "host_name":         {"type": "string"},
                    "host_BioGuideID":   {"type": ["string","null"]},
                    "host_party":        {"type": "string"},
                    "host_homeCD":       {"type": "integer"},
                    "CD_MC":             {"type": ["string","null"]},
                    "CD_MC_bioguideID":  {"type": ["string","null"]},
                    "CD_hostvoteshare":  {"type": ["number","null"]},
                    "CD_Dpresvoteshare": {"type": ["number","null"]},
                    "host_vulnerable":   {"type": ["integer","null"]},
                    "notes":             {"type": ["string","null"]},
                },
            },
        },
    },
}
