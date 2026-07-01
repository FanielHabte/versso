from dataclasses import dataclass


@dataclass(frozen=True)
class UserPayload:
    user_id: str
    name_space: str
    aws_account_id: str
    user_name: str
