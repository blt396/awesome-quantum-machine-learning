#!/usr/bin/env python3
"""
URL Health Checker for README.md.
Extracts all URLs in README.md and sends HTTP requests to verify status.
"""

import re
import sys
import ssl
import urllib.request
import urllib.error
from pathlib import Path


def check_urls(file_path: Path) -> bool:
    if not file_path.exists():
        print(f"Error: {file_path} does not exist.")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Extract markdown links: [Name](URL) ignoring pure badges/anchors
    url_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    raw_matches = url_pattern.findall(content)

    # Filter out embedded badge image syntax like [![Awesome](url)
    matches = []
    for name, url in raw_matches:
        clean_name = name.replace("![", "").strip()
        matches.append((clean_name, url))

    if not matches:
        print("No HTTP/HTTPS URLs found in file.")
        return True

    print(f"Checking {len(matches)} URLs in {file_path.name}...\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Disable SSL context verification for legacy server cert checks
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    broken_urls = []
    valid_urls = []

    for name, url in matches:
        safe_name = name.encode("ascii", errors="replace").decode("ascii")
        success = False
        last_error = ""

        # Try up to 2 times in case of transient network delays
        for attempt in range(2):
            req = urllib.request.Request(url, headers=headers, method="GET")
            try:
                with urllib.request.urlopen(req, timeout=25, context=ctx) as response:
                    status = response.getcode()
                    if status < 400:
                        valid_urls.append((safe_name, url, status))
                        print(f" [OK {status}] {safe_name} -> {url}", flush=True)
                        success = True
                        break
                    else:
                        last_error = f"HTTP {status}"
            except urllib.error.HTTPError as e:
                if e.code == 403 and any(domain in url for domain in ["slack.com", "amazon.com", "sciencedirect.com", "stackexchange.com"]):
                    valid_urls.append((safe_name, url, f"HTTP 403 (Active, bot-protected)"))
                    print(f" [OK 403 Bot-Protected] {safe_name} -> {url}", flush=True)
                    success = True
                    break
                else:
                    last_error = f"HTTP {e.code}"
            except urllib.error.URLError as e:
                last_error = f"URL Error: {e.reason}"
            except Exception as e:
                last_error = f"Error: {str(e)}"

        if not success:
            broken_urls.append((safe_name, url, last_error))
            print(f" [FAIL] {safe_name} -> {url} ({last_error})", flush=True)

    print("\n" + "=" * 60)
    print(f"Total checked: {len(matches)} | Valid: {len(valid_urls)} | Broken: {len(broken_urls)}")
    print("=" * 60 + "\n")

    if broken_urls:
        print("Broken URLs Summary:")
        for name, url, reason in broken_urls:
            print(f"- [{name}]({url}): {reason}")
        return False

    print("All URLs verified successfully!")
    return True


if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / "README.md"
    success = check_urls(readme_path)
    if not success:
        sys.exit(1)
    sys.exit(0)
