from typing import List, Literal
from pydantic import StrictBool, StrictInt, BaseModel
from dtos.base.data_types import StrPopulated, DatetimeIso8601, DateYmd
from dtos.moxfield.moxfield_basemodel import MoxFieldBaseModel
from debug import *

class TestObj(BaseModel):
    access_token: StrPopulated
    refresh_token: StrPopulated

# var = '{"access_token": "asdasd", "refresh_token": "aaaaa"}'
var = {"access_token": "asdasd", "refresh_token": "aaaaa"}

output = TestObj.parse_raw(var)
pvdd(output)

class RefreshTokenResponseDto(MoxFieldBaseModel):
    access_token: StrPopulated
    refresh_token: StrPopulated
    token_type: Literal["Bearer"]
    user_name: StrPopulated
    email_address: StrPopulated
    is_email_confirmed: StrictBool
    expiration: DatetimeIso8601
    expires_in_minutes: StrictInt
    permissions: List[StrPopulated]
    user_id: StrPopulated
    nolt_token: StrPopulated
    mature_content_pref: StrPopulated
    date_of_birth: DateYmd
