from enum import Enum
from typing import List, Dict, TypeAlias

from pydantic import BaseModel
from square_commons.api_utils import StandardResponse


class TokenType(Enum):
    access_token = "access_token"
    refresh_token = "refresh_token"


class RegisterUsernameV0ResponseMain(BaseModel):
    user_id: str
    username: str
    app_id: int | None
    access_token: str | None
    refresh_token: str | None
    refresh_token_expiry_time: str | None


class RegisterUsernameV0Response(BaseModel):
    main: RegisterUsernameV0ResponseMain


class RegisterLoginGoogleV0ResponseMain(BaseModel):
    user_id: str
    username: str
    app_id: int | None
    access_token: str | None
    refresh_token: str | None
    refresh_token_expiry_time: str | None
    was_new_user: bool


class RegisterLoginGoogleV0Response(BaseModel):
    main: RegisterLoginGoogleV0ResponseMain


class LoginUsernameV0ResponseMain(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    refresh_token_expiry_time: str


class LoginUsernameV0Response(BaseModel):
    main: LoginUsernameV0ResponseMain


class UpdateUserAppIdsV0Response(BaseModel):
    main: List[int]


class GetUserDetailsV0ResponseMainProfile(BaseModel):
    user_profile_id: int
    user_profile_photo_storage_token: str | None
    user_profile_email: str | None
    user_profile_phone_number_country_code: str | None
    user_profile_phone_number: str | None
    user_profile_first_name: str | None
    user_profile_last_name: str | None
    user_profile_email_verified: str | None


class GetUserDetailsV0ResponseMainSession(BaseModel):
    app_name: str
    active_sessions: int


class GetUserDetailsV0ResponseMainEmailVerification(BaseModel):
    expires_at: str
    cooldown_reset_at: str


class GetUserDetailsV0ResponseMainBackupCodes(BaseModel):
    total: int
    available: int
    generated_at: str


class GetUserDetailsV0ResponseMain(BaseModel):
    user_id: str
    username: str
    profile: GetUserDetailsV0ResponseMainProfile
    apps: List[str]
    sessions: List[GetUserDetailsV0ResponseMainSession]
    recovery_methods: Dict[str, bool]
    email_verification_details: GetUserDetailsV0ResponseMainEmailVerification | None
    backup_code_details: GetUserDetailsV0ResponseMainBackupCodes | None


class GetUserDetailsV0Response(BaseModel):
    main: GetUserDetailsV0ResponseMain


class GenerateAccessTokenV0ResponseMain(BaseModel):
    access_token: str


class GenerateAccessTokenV0Response(BaseModel):
    main: GenerateAccessTokenV0ResponseMain


LogoutV0Response: TypeAlias = StandardResponse[None]
LogoutAppsV0Response: TypeAlias = StandardResponse[None]
LogoutAllV0Response: TypeAlias = StandardResponse[None]


class UpdateUsernameV0ResponseMain(BaseModel):
    user_id: str
    username: str


class UpdateUsernameV0Response(BaseModel):
    main: UpdateUsernameV0ResponseMain


DeleteUserV0Response: TypeAlias = StandardResponse[None]
UpdatePasswordV0Response: TypeAlias = StandardResponse[None]


class ValidateAndGetPayloadFromTokenV0Response(BaseModel):
    main: dict


class UpdateUserRecoveryMethodsV0Response(BaseModel):
    main: List[str]


class GenerateAccountBackupCodesV0ResponseMain(BaseModel):
    user_id: str
    backup_codes: List[str]


class GenerateAccountBackupCodesV0Response(BaseModel):
    main: GenerateAccountBackupCodesV0ResponseMain


class ResetPasswordAndLoginUsingBackupCodeV0ResponseMain(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    refresh_token_expiry_time: str


class ResetPasswordAndLoginUsingBackupCodeV0Response(BaseModel):
    main: ResetPasswordAndLoginUsingBackupCodeV0ResponseMain


class SendResetPasswordEmailV0Response(BaseModel):
    expires_at: str
    cooldown_reset_at: str


class ResetPasswordAndLoginUsingResetEmailCodeV0ResponseMain(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    refresh_token_expiry_time: str


class ResetPasswordAndLoginUsingResetEmailCodeV0Response(BaseModel):
    main: ResetPasswordAndLoginUsingResetEmailCodeV0ResponseMain


class GetUserRecoveryMethodsV0Response(BaseModel):
    main: Dict[str, bool]


class SendVerificationEmailV0Response(BaseModel):
    expires_at: str
    cooldown_reset_at: str


class UpdateProfilePhotoV0Response(BaseModel):
    main: str | None


class UpdateProfileDetailsV0ResponseMain(BaseModel):
    user_profile_photo_storage_token: str | None
    user_profile_email: str | None
    user_profile_phone_number_country_code: str | None
    user_profile_first_name: str | None
    user_profile_last_name: str | None
    user_id: str
    user_profile_id: int
    user_profile_email_verified: str | None
    user_profile_phone_number: str | None


class UpdateProfileDetailsV0Response(BaseModel):
    main: list[UpdateProfileDetailsV0ResponseMain]
    affected_count: int


class ValidateEmailVerificationCodeV0Response(BaseModel):
    user_profile_email_verified: str
