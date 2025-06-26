from signal import signal, SIGINT
from core.logger import log


class GracefulShutdown:
    """
    Handles SIGINT (Ctrl+C) signal to gracefully stop the application.
    """

    def __init__(self):
        """
        Initialize the shutdown flag and register the SIGINT handler.
        """
        self.shutdown = False
        signal(SIGINT, self._handle_exit)

    def _handle_exit(self, signum: int, frame) -> None:
        """
        Internal signal handler to set shutdown flag.

        Args:
            signum: Signal number.
            frame: Current stack frame (unused).
        """
        log.info("Shutting down…")
        self.shutdown = True
