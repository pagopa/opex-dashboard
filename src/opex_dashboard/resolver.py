import prance

from typing import Dict, Any
from prance.util.resolver import RESOLVE_FILES

from opex_dashboard.error import ParseError

PARSER_BACKEND = "openapi-spec-validator"


class OA3Resolver:
    _resolver: prance.ResolvingParser

    def __init__(self, path: str) -> None:
        """Create an OA3Resolver object
        """
        self._resolver = prance.ResolvingParser(
            path,
            backend=PARSER_BACKEND,
            resolve_types=RESOLVE_FILES,
            lazy=True,
            strict=False
        )

    def resolve(self) -> Dict[str, Any]:
        """Resolve OpenAPI specification with Prance's ResolvingParser

        Returns:
            Dict: Parsed spec as a dictionary

        Raises:
            ParseError: If some validation or parsing error occurred
        """
        try:
            self._resolver.parse()
            return self._resolver.specification
        except prance.ValidationError as error:
            raise ParseError(f"OA3 validation error: {error}")
        except prance.util.formats.ParseError as error:
            raise ParseError(f"OA3 parsing error: {error}")
