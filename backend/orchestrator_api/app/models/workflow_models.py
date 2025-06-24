from pydantic import BaseModel

class ImportWorkflowRequest(BaseModel):
    name: str
    definition: dict

class TriggerWorkflowRequest(BaseModel):
    webhookName: str
    payload: dict
