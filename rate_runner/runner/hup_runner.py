import logging

from .base import BaseRunner

logger = logging.getLogger(__name__)

# Alias for the callback that will be invoked after each batch is complete
BatchCompleteCallback = Callable[[dict], None]

class HeavyIonRunner(BaseRunner):

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
        self.session = session
        self.on_batch_complete = on_batch_complete

        # These must be set by set_environment() before a run can be performed.
        self._file_name = None
        self._file_uid = None
        self._comment = None

        # Internal collection of parts, effects, and cross sections to run HUP rates for
        self._parts = []


    def set_environment(self, *, file_name: str, file_uid: str, comment: Optional[str] = None) -> None:
        """Sets the CREME96 LET spectrum to use for the next run

        The `file_name` and `file_uid` must match the values assigned by the CREME96 site when the
        LET spectrum was created using the LETSPEC module. These correspond to the `letFileId` and
        `letFileId_UID` fields in the POST form submitted when invoking the HUP module.

        Args:
            file_name (str): Filename of the LETSPEC file to use
            file_uid (str): UID of the corresponding LETSPEC file
            comment (Optional[str]): User defined label for tracking or display

        """
        self._file_name = file_name
        self._file_uid = file_uid
        self._comment = comment
        logger.info("Environment set to file '%s' (UID: %s)", self._file_name, self._file_uid)

    def add_part(self, part: dict) -> None:
        """Adds a heavy ion cross section element to the list of devices to run rates for

        Raises:
            ValueError: If required fields are missing or invalid values were provided

        """
        validate_part(part)
        self._parts.append(part)
        logger.debug("Added device: %s", part["device"])

    def add_parts(self, parts: list[dict]) -> None:
        """Adds a list of heavy ion cross section elements to the list of devices to run rates for

        Raises:
            ValueError: If required fields are missing or invalid values were provided

        """
        for part in parts:
            validate_part(part)
            self._parts.append(part)
            logger.debug("Added device: %s", part["device"])

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
