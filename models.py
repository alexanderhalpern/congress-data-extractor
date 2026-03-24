from typing import Optional
from pydantic import BaseModel


class HearingData(BaseModel):
    hearingID: str
    date: str
    title: str
    topic: str
    committee: str
    subcommitteee: int
    subcomittee_name: Optional[str]
    chamber: str
    majparty: str
    congress: int
    midterm: int
    location_city: str
    location_CD: str
    location_type: str
    host: str
    host2: Optional[str]
    host_homeCD: Optional[int]
    open: int
    num_witnesses: int
    num_MCs: int
    D_present: int
    R_present: int
    chair_present: int
    subcommitteechair_present: Optional[int]
    ratio_present: Optional[float]
    pdfname: str
    notes: Optional[str]


class WitnessData(BaseModel):
    hearingID: str
    witness_name: str
    witness_occupation: str
    witness_rep: str
    witness_type: str
    speaking_order: int
    agreement_chair: Optional[str]
    notes: Optional[str]


class MemberData(BaseModel):
    hearingID: str
    host_name: str
    host_BioGuideID: Optional[str]
    host_party: str
    host_homeCD: Optional[int]
    CD_MC: Optional[str]
    CD_MC_bioguideID: Optional[str]
    CD_hostvoteshare: Optional[float]
    CD_Dpresvoteshare: Optional[float]
    host_vulnerable: Optional[int]
    notes: Optional[str]


class LLMResult(BaseModel):
    sufficient_data: bool
    missing_reason: Optional[str]
    hearing: HearingData
    witnesses: list[WitnessData]
    members: list[MemberData]
