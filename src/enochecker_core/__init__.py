__all__ = [
    "CheckerTaskResult",
    "CheckerMethod",
    "CheckerHealthStatus",
    "CheckerInfoMessage",
    "CheckerResultMessage",
    "CheckerHealthMessage",
    "EnoLogMessage",
    "CheckerTaskMessage",
]

from enum import Enum
from typing import Any
from pydantic.alias_generators import to_camel
from pydantic import (
    AliasGenerator,
    BaseModel as PydanticBaseModel,
    ConfigDict,
    model_validator,
)


class CheckerTaskResult(str, Enum):
    OK = "OK"
    MUMBLE = "MUMBLE"
    OFFLINE = "OFFLINE"
    INTERNAL_ERROR = "INTERNAL_ERROR"

    def __str__(self) -> str:
        return self.value


class CheckerMethod(str, Enum):
    PUTFLAG = "putflag"
    GETFLAG = "getflag"
    PUTNOISE = "putnoise"
    GETNOISE = "getnoise"
    HAVOC = "havoc"
    EXPLOIT = "exploit"
    TEST = "test"

    def __str__(self) -> str:
        return self.value


class CheckerHealthStatus(str, Enum):
    OK = "ok"
    ERROR = "error"

    def __str__(self) -> str:
        return self.value


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        alias_generator=AliasGenerator(alias=to_camel),
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )


class CheckerInfoMessage(BaseModel):
    service_name: str
    flag_variants: int
    noise_variants: int
    havoc_variants: int
    # Indexed by exploit variant id, each entry is the flag variant (flag store)
    # that exploit targets, so the length is the number of exploit variants.
    exploit_variants: list[int]
    test_variants: int = 0

    @model_validator(mode="after")
    def _validate_exploit_variants(self) -> "CheckerInfoMessage":
        for exploit_variant_id, flag_variant_id in enumerate(self.exploit_variants):
            if not 0 <= flag_variant_id < self.flag_variants:
                raise ValueError(
                    f"exploit variant {exploit_variant_id} targets flag variant "
                    f"{flag_variant_id}, which is not in range(0, {self.flag_variants})"
                )

        return self


class CheckerResultMessage(BaseModel):
    result: CheckerTaskResult
    message: str | None = None
    attack_info: str | None = None
    flag: str | None = None
    # Free-form JSON-serializable data outside the checker spec.
    metadata: dict[str, Any] | None = None


class CheckerHealthMessage(BaseModel):
    # A checker may report implementation-specific fields next to the status,
    # so a consumer validating this model keeps them instead of dropping them.
    model_config = ConfigDict(extra="allow")

    status: CheckerHealthStatus
    detail: str | None = None


class CheckerTaskMessage(BaseModel):
    task_id: int
    method: CheckerMethod
    address: str
    team_id: int
    team_name: str
    current_round_id: int
    related_round_id: int
    flag: str | None = None
    variant_id: int
    timeout: int
    round_length: int
    task_chain_id: str
    flag_regex: str | None = None
    flag_hash: str | None = None
    attack_info: str | None = None
    # Optional, caller-supplied seed for checker PRNG. Makes random checker
    # behavior reproducible.
    seed: str | None = None


class EnoLogMessage(BaseModel):
    tool: str
    type: str
    severity: str
    severity_level: int
    timestamp: str
    message: str
    module: str | None
    function: str | None
    service_name: str | None
    task_id: int | None
    method: str | None
    team_id: int | None
    team_name: str | None
    current_round_id: int | None
    related_round_id: int | None
    flag: str | None
    variant_id: int | None
    task_chain_id: str | None
    flag_regex: str | None
    flag_hash: str | None
    attack_info: str | None
