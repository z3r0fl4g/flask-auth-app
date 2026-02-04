"""Utility for capturing 2FA codes from Flask console output."""
import re
import time
from typing import Optional


def extract_2fa_code(log_output: str, email: Optional[str] = None) -> Optional[str]:
    """Extract 2FA verification code from Flask console output.

    The Flask app prints verification codes in the format:
    VERIFICATION CODE: 123456

    Args:
        log_output: The captured console/log output string
        email: Optional email to filter by (for future use if log format changes)

    Returns:
        The 6-digit verification code as a string, or None if not found
    """
    # Primary pattern: VERIFICATION CODE: XXXXXX
    pattern = r'VERIFICATION CODE:\s*(\d{6})'
    match = re.search(pattern, log_output, re.IGNORECASE)

    if match:
        return match.group(1)

    # Alternative patterns (in case log format varies)
    alt_patterns = [
        r'verification\s+code[:\s]+(\d{6})',
        r'code[:\s]+(\d{6})',
        r'2FA\s+code[:\s]+(\d{6})',
        r'OTP[:\s]+(\d{6})',
    ]

    for pattern in alt_patterns:
        match = re.search(pattern, log_output, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def extract_latest_2fa_code(log_output: str) -> Optional[str]:
    """Extract the most recent 2FA code from log output.

    When multiple codes are present (e.g., from resend), returns the last one.

    Args:
        log_output: The captured console/log output string

    Returns:
        The most recent 6-digit verification code, or None if not found
    """
    pattern = r'VERIFICATION CODE:\s*(\d{6})'
    matches = re.findall(pattern, log_output, re.IGNORECASE)

    if matches:
        return matches[-1]  # Return the most recent code

    return None


class FlaskLogCapture:
    """Context manager for capturing Flask subprocess output.

    Usage:
        with FlaskLogCapture(flask_process) as capture:
            # Trigger action that generates 2FA code
            code = capture.wait_for_code(timeout=10)
    """

    def __init__(self, process):
        """Initialize with subprocess.Popen object.

        Args:
            process: The Flask subprocess with stdout/stderr captured
        """
        self.process = process
        self.captured_output = ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read_output(self) -> str:
        """Read available output from the subprocess."""
        import select
        import os

        if self.process.stdout:
            # Non-blocking read
            if hasattr(select, 'select'):
                readable, _, _ = select.select([self.process.stdout], [], [], 0.1)
                if readable:
                    try:
                        data = os.read(self.process.stdout.fileno(), 4096)
                        self.captured_output += data.decode('utf-8', errors='replace')
                    except (OSError, IOError):
                        pass

        return self.captured_output

    def wait_for_code(self, timeout: int = 10) -> Optional[str]:
        """Wait for a 2FA code to appear in the output.

        Args:
            timeout: Maximum seconds to wait for a code

        Returns:
            The 6-digit verification code, or None if timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            self.read_output()
            code = extract_latest_2fa_code(self.captured_output)
            if code:
                return code
            time.sleep(0.5)

        return None

    def get_all_output(self) -> str:
        """Get all captured output."""
        self.read_output()
        return self.captured_output


def wait_for_2fa_code_in_file(log_file_path: str, timeout: int = 10) -> Optional[str]:
    """Wait for a 2FA code to appear in a log file.

    Useful when Flask logs to a file instead of stdout.

    Args:
        log_file_path: Path to the Flask log file
        timeout: Maximum seconds to wait

    Returns:
        The 6-digit verification code, or None if timeout
    """
    start_time = time.time()
    last_position = 0

    while time.time() - start_time < timeout:
        try:
            with open(log_file_path, 'r') as f:
                f.seek(last_position)
                new_content = f.read()
                last_position = f.tell()

                code = extract_2fa_code(new_content)
                if code:
                    return code
        except FileNotFoundError:
            pass

        time.sleep(0.5)

    return None
