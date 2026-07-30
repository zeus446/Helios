from pydantic import BaseModel, ConfigDict

class PreferencesCreate(BaseModel):
    job_title:str
    location:str
    remote_only:bool
    employment_type:str


class PreferencesResponse(BaseModel):
    id:int
    user_id:int
    job_title:str
    location:str
    remote_only:bool
    employment_type:str

    model_config = ConfigDict(from_attributes=True)
