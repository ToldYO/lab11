from typing import Optional
import re

from presidio_anonymizer.operators import Operator, OperatorType


class Initial(Operator):
    """
    Initial operator:
    - For each whitespace-separated token, collapse whitespace across the text first.
    - For each token, preserve any leading non-alphanumeric prefix, find the first
      alphanumeric character, and turn that into the initial (uppercase for letters).
      Everything after the first alphanumeric is not carried over.
    Examples:
      "John Smith" -> "J. S."
      "   Eastern   Michigan  University " -> "E. M. U."
      "@abc" -> "@A."
      "@843A" -> "@8."
      "--**abc" -> "--**A."
    """

    def operator_name(self) -> str:
        return "initial"

    def operator_type(self):
        return OperatorType.Anonymize

    def validate(self, params: dict = None):
        # No parameters to validate for now.
        pass

    def operate(self, text: Optional[str] = None, params: dict = None) -> Optional[str]:
        if text is None:
            return text

        # Collapse consecutive whitespace into a single space and trim ends
        collapsed = re.sub(r"\s+", " ", text).strip()

        if collapsed == "":
            return collapsed

        tokens = collapsed.split(" ")

        processed_tokens = []
        for token in tokens:
            # find first alphanumeric character index
            first_alnum_idx = None
            for i, ch in enumerate(token):
                if ch.isalnum():
                    first_alnum_idx = i
                    break

            if first_alnum_idx is None:
                # no alphanumeric character in token — keep token as-is
                processed_tokens.append(token)
                continue

            prefix = token[:first_alnum_idx]  # keep everything before first alnum
            first_alnum_char = token[first_alnum_idx]

            # Uppercase letters; digits kept as-is
            if first_alnum_char.isalpha():
                initial_char = first_alnum_char.upper()
            else:
                initial_char = first_alnum_char

            # build replaced token: prefix + initial + "."
            new_token = f"{prefix}{initial_char}."
            processed_tokens.append(new_token)

        return " ".join(processed_tokens)
