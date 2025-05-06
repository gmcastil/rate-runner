from typing import Tuple, List, Dict, Any
from typing import Callable, Optional
import logging

import requests

from rate_runner import constants
from .base import BaseRunner

logger = logging.getLogger(__name__)

# Alias for the callback that will be invoked after each batch is complete
BatchCompleteCallback = Callable[[dict], None]

class HeavyIonRunner(BaseRunner):

    # The CREME96 backend only allows rates to be run for this many devices at a time
    MAX_BATCH_SIZE = 10

    def __init__(self, session: requests.Session,
                 on_batch_complete: Optional[BatchCompleteCallback] = None):
        """ Initializes the heavy ion runner

        Args:
            session: Authenticated CREME96 session
            on_batch_complete (Optional[Callable[[dict], None]]): Optional callback
                invoked after each batch is submitted. Called with a dictionary:

                    {
                        TBD
                    }
        """
        logger.info("Creating heavy ion runner")
        self._session = session
        self._on_batch_complete = on_batch_complete

        # These must be set by set_environment() before a run can be performed.
        self._file_name = None
        self._file_uid = None
        self._comment = None

        # Internal collection of parts, effects, and cross sections to run HUP rates for
        self._parts = []

    def set_environment(self, *, file_name: str, file_uid: str, desc: Optional[str] = None) -> None:
        """Sets the CREME96 LET spectrum to use for the next run

        The `file_name` and `file_uid` must match the values assigned by the CREME96 site when the
        LET spectrum was created using the LETSPEC module. These correspond to the `letFileId` and
        `letFileId_UID` fields in the POST form submitted when invoking the HUP module. The `desc`
        field is provided for convenience and is unused by CREME96.

        Args:
            file_name (str): Filename of the LETSPEC file to use
            file_uid (str): UID of the corresponding LETSPEC file
            desc (Optional[str]): User defined description tracking or display

        """
        self._file_name = file_name
        self._file_uid = file_uid
        self._desc = desc
        logger.info("Environment set to file '%s' (UID: %s)", self._file_name, self._file_uid)

    def add_part(self, part: Dict[str, Any]) -> None:
        """Adds a heavy ion cross section element to the list of devices to run rates for

        Raises:
            ValueError: If required fields are missing or invalid values were provided

        """
        validate_part(part)
        self._parts.append(part)
        logger.debug("Added device: %s", part["device"])

    def add_parts(self, parts: List[Dict[str, Any]]) -> None:
        """Adds a list of heavy ion cross section elements to the list of devices to run rates for

        Raises:
            ValueError: If required fields are missing or invalid values were provided

        """
        for part in parts:
            validate_part(part)
            self._parts.append(part)
            logger.debug("Added device: %s", part["device"])

    def run(self) -> None:
        """Submits loaded cross sections to CREME96 for rate calculation in the current environment

        Raises:
            RuntimeError: If no parts have been added or the environment has not been configured
                using `set_environment()`
            requests.HTTPError: If the submission to CREME96 fails
            ValueError: If the server response cannot be parsed or is malformed

        """
        self._validate_ready()
        # Break into MAX_BATCH_SIZE lists of parts 
        batches = [self._parts[i:i+MAX_BATCH_SIZE] for i in range(0, len(self._parts), MAX_BATCH_SIZE)]

        run_results = []

        # Submit each batch of parts and append results
        for index, batch in enumerate(batches):

            # Build the POST payload for this batch of cross sections
            payload = self._build_payload(batch)

            # Submit this batch of parts to CREME96 for calculation
            response = self._submit_batch(payload)

            # Parse response and store
            batch_result = self._parse_response(response)
            run_results.extend(batch_result)

            # Progress callback if set
            if self._on_batch_complete:
                self._on_batch_complete()

        # Store all results for this environment for retrieval later
        self._results.append({
            "file_name": self._file_name,
            "file_uid": self._file_uid,
            "desc": self._desc,
            "num_parts": len(self._parts),
            "results": run_results
        })

    def _validate_ready(self) -> None:
        """Raises an exception if the runner is not ready actually call `run()`"""
        if not self._parts:
            raise RuntimeError("No parts have been added to HUP runner")
        if self._file_uid is None or self._file_name is None:
            raise RuntimeError("LET spectrum has not been set")

    def _build_payload(self, batch: List[Dict[str, str]]) -> dict:
        """Constructs a CREME96 HUP template compatible form submission

        Takes a batch of up to 10 parts and constructs a POST-compatible dictionary matching the field
        names and structure expected by the CREME96 submission form.

        Args:
            batch (list[dict]): 1-10 validated heavy ion cross section dictionaries

        Returns:
            List[Tuple[str, str]]: Payload of flattened part values for HupTemplate form

        """

        # Define a table containing the POST form field name, the key name in the dict of each part,
        # and a function to convert each field appropriately. The POST field names need to match
        # what CREME96 front end sends as part of the 'HupTemplate' (e.g., fields like `letFileId`).
        hup_field_specs = [
                ("label:list", "label", str),
                ("comment1:list", "comment1", str),
                ("comment2:list", "comment2", str),
                ("rppx:list", "rppx", lambda v: str(float(v))),
                ("rppy:list", "rppy", lambda v: str(float(v))),
                ("rppz:list", "rppz", lambda v: str(float(v))),
                ("funnel:list", "funnel", lambda v: str(float(v))),
                ("bitsPerDevice:list", "bitsPerDevice", lambda v: str(float(v))),
                ("onset:list", "onset", str),
                ("width:list", "width", str),
                ("exponent:list", "exponent", str),
                ("limitingXS:list", "limitingXS", str),
                ("qcrit:list", "qcrit", str),
                ("xsPerBit:list", "xsPerBit", str),
        ]

        # Global fields
        payload = [
                ("letFileId", self._file_name),
                ("letFileId_UID", self._file_uid),
                ("jobName", constants.HUP_RESULT_JOB)
        ]

        # Per-part fields
        for form_key, part_key, convert in field_specs:
            for i in range(MAX_BATCH_SIZE):
                value = parts[i].get(part_key, "") if i < len(parts) else ""
                try:
                    payload.append((form_key, convert(value) if value != "" else ""))
                except Exception:
                    payload.append((form_key, ""))

        for i in range(10):
            value = parts[i].get("xsInputMethod", "") if i < len(parts) else ""
            payload.append((f"xsInputMethod{i}", str(value)))

        # Trailing fields
        payload.extend([
            ("form.button.submit", "Submit"),
            ("FormType", "Hup"),
            ("FormSessionData", "HupForm"),
            ("form.submitted", "1"),
            ("tzoffset", "360"),
        ])

    def _submit_batch(self, payload: List[Tuple[str, str]]) -> requests.Response:
        """Submits a batch payload to CREME96

        Args:
            payload (List[Tuple[str, str]]): Form-encoded POST data as a list of (key, value) pairs
            including repeated fields for each part

        Returns:
            requests.Response: The HTTP response object from CREME96

        Raises:
            requests.HTTPError

        """
        response = self._session.post(CREME96_HUP_SUBMIT_URL, data=payload)
        response.raise_for_status()

def validate_part(part: dict) -> None:
    """Validates a heavy ion cross section element

    Checks that the heavy ion cross section that is provided is internally consistent and provides
    the appropriate values.  Note that only Weibull or critical charge cross section parameters are
    supported.

    Args:
        part (dict): Heavy ion cross section element

    Raises:
        ValueError: If required fields are missing or invalid values were provided

    """
    return None

