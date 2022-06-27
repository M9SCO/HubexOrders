from typing import Optional

from pydantic import BaseModel


class HubexHookCreateTask(BaseModel):
    TenantID: int
    TaskID: int
    AssetID: int
    TaskConversationID: Optional[int]
    TenantMemberID: Optional[int]
    AccountID: Optional[int]
    UserID: Optional[int]
    CompanyID: Optional[int]
    EventID: Optional[int]
    TaskStageID: Optional[int]
