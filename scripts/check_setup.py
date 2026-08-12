#!/usr/bin/env python3
"""Verify everything needed to generate Poptastic panels is in place.

Run this before the first generation of a session. It checks the four things that
actually break: the SDK, the key, network reachability, and model access (which is
gated behind OpenAI's organization verification).
"""
import os
import sys

OK, BAD, WARN = "  OK  ", " FAIL ", " WARN "


def line(status, msg, fix=None):
    print(f"[{status}] {msg}")
    if fix:
        print(f"         -> {fix}")


def main():
    failures = 0

    # 0. Python version. The scripts target 3.9+, but flag anything older.
    v = sys.version_info
    if (v.major, v.minor) < (3, 9):
        line(BAD, f"Python {v.major}.{v.minor} is too old",
             "install Python 3.9 or newer from python.org")
        return 1
    line(OK, f"Python {v.major}.{v.minor}.{v.micro}")

    # 1. SDK
    try:
        import openai  # noqa: F401
        line(OK, f"openai SDK installed (v{openai.__version__})")
    except ImportError:
        line(BAD, "openai SDK not installed", "pip install openai pillow")
        return 1

    try:
        from PIL import Image  # noqa: F401
        line(OK, "Pillow installed")
    except ImportError:
        line(BAD, "Pillow not installed", "pip install pillow")
        failures += 1

    # 2. Key
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        line(BAD, "OPENAI_API_KEY is not set",
             'export OPENAI_API_KEY="sk-..."  (add to ~/.zshrc to persist)')
        return 1
    if not key.startswith("sk-"):
        line(WARN, "OPENAI_API_KEY does not start with 'sk-' — check it was copied whole")
    else:
        line(OK, f"OPENAI_API_KEY found ({key[:7]}...{key[-4:]})")

    # 3 + 4. Network and model access, in one cheap real call.
    from openai import OpenAI
    client = OpenAI()
    try:
        client.models.retrieve("gpt-image-2")
        line(OK, "gpt-image-2 is reachable and available to this organization")
    except Exception as e:
        text = str(e).lower()
        if "connect" in text or "network" in text or "timed out" in text:
            line(BAD, "cannot reach api.openai.com",
                 "this environment blocks outbound network access — run the generator "
                 "somewhere with internet, e.g. your own terminal")
        elif "401" in text or "authentication" in text or "invalid_api_key" in text:
            line(BAD, "key rejected", "regenerate the key at platform.openai.com")
        elif "403" in text or "not found" in text or "does not exist" in text:
            line(BAD, "no access to gpt-image-2",
                 "complete API Organization Verification: platform.openai.com -> "
                 "Settings -> Organization -> General")
        else:
            line(BAD, f"unexpected error: {e}")
        failures += 1

    print()
    if failures:
        print("Setup incomplete. See references/API_SETUP.md.")
        return 1
    print("Ready to generate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
