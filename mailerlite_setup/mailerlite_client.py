"""
Minimal MailerLite REST client for the funnel setup.
Uses the v2 Connect API at https://connect.mailerlite.com/api
"""

import os
import time
import requests
from typing import Any


class MailerLite:
    BASE = "https://connect.mailerlite.com/api"

    def __init__(self, api_key: str):
        if not api_key or api_key == "your_api_key_here":
            raise ValueError(
                "Missing MAILERLITE_API_KEY. Set it in mailerlite_setup/.env"
            )
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        url = f"{self.BASE}{path}"
        for attempt in range(3):
            r = self.session.request(method, url, timeout=30, **kwargs)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 5))
                print(f"   ⏳ rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            if r.status_code >= 400:
                detail = r.text[:400]
                raise RuntimeError(f"{method} {path} → {r.status_code}: {detail}")
            if r.status_code == 204:
                return {}
            return r.json()
        raise RuntimeError("Too many retries")

    # ── GROUPS ──────────────────────────────────────────────
    def list_groups(self) -> list[dict]:
        return self._request("GET", "/groups").get("data", [])

    def find_group(self, name: str) -> dict | None:
        for g in self.list_groups():
            if g["name"] == name:
                return g
        return None

    def create_group(self, name: str) -> dict:
        return self._request("POST", "/groups", json={"name": name})["data"]

    def get_or_create_group(self, name: str) -> dict:
        existing = self.find_group(name)
        if existing:
            print(f"   ↻ Group '{name}' already exists (id={existing['id']})")
            return existing
        created = self.create_group(name)
        print(f"   ✓ Created group '{name}' (id={created['id']})")
        return created

    # ── CUSTOM FIELDS ──────────────────────────────────────
    def list_fields(self) -> list[dict]:
        return self._request("GET", "/fields").get("data", [])

    def find_field(self, name: str) -> dict | None:
        for f in self.list_fields():
            if f["name"] == name:
                return f
        return None

    def create_field(self, name: str, field_type: str = "text") -> dict:
        # field_type one of: text, number, date
        return self._request(
            "POST", "/fields",
            json={"name": name, "type": field_type}
        )["data"]

    def get_or_create_field(self, name: str, field_type: str = "text") -> dict:
        existing = self.find_field(name)
        if existing:
            print(f"   ↻ Field '{name}' already exists")
            return existing
        created = self.create_field(name, field_type)
        print(f"   ✓ Created field '{name}'")
        return created

    # ── CAMPAIGNS (drafts) ─────────────────────────────────
    def create_campaign(self, *, name: str, subject: str, from_email: str,
                        from_name: str, content_html: str,
                        group_ids: list[str] | None = None) -> dict:
        """Create a regular email campaign as draft.
        If group_ids is provided, the campaign targets those groups."""
        payload = {
            "name": name,
            "type": "regular",
            "emails": [{
                "subject": subject,
                "from": from_email,
                "from_name": from_name,
                "content": content_html,
            }],
        }
        if group_ids:
            payload["groups"] = group_ids
        return self._request("POST", "/campaigns", json=payload)["data"]

    def list_campaigns(self) -> list[dict]:
        return self._request("GET", "/campaigns").get("data", [])

    # ── AUTOMATIONS ────────────────────────────────────────
    def list_automations(self) -> list[dict]:
        return self._request("GET", "/automations").get("data", [])

    def find_automation(self, name: str) -> dict | None:
        for a in self.list_automations():
            if a.get("name") == name:
                return a
        return None

    def create_automation_draft(self, name: str) -> dict:
        return self._request("POST", "/automations", json={"name": name})["data"]

    def get_or_create_automation(self, name: str) -> dict:
        existing = self.find_automation(name)
        if existing:
            return existing
        return self.create_automation_draft(name)
