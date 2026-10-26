# enochecker_core

Python library providing typed message models (dataclasses and enums) for the
ENOchecker task protocol.

## Install

```
pip install enochecker-core
```

Requires Python ≥ 3.10.

Minor versions are (usually) bumped in sync with
[enochecker3](https://github.com/attacking-lab/enochecker3).

## Usage

```python
from enochecker_core import (
    CheckerMethod, CheckerTaskResult,
    CheckerTaskMessage, CheckerResultMessage, CheckerInfoMessage,
    CheckerHealthMessage, CheckerHealthStatus, EnoLogMessage,
)
```

All models are Pydantic `BaseModel` subclasses. Fields are camelCase in
JSON and snake_case in Python. Serialize with `model_dump_json()`, deserialize
with `Model.model_validate_json(...)`.

## License

MIT - see [LICENSE](LICENSE).
