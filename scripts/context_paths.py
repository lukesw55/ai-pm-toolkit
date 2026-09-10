"""Shared project identity and path boundary for context writers."""
import re
from pathlib import Path

SLUG_RE = re.compile(r"[a-z0-9][a-z0-9-]*")
PII_DENY = ("raw-evidence", "people", "data")


def validate_slug(slug):
    if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
        raise ValueError("invalid project slug: use lowercase letters, digits and hyphens")
    if slug in PII_DENY:
        raise ValueError("refusing PII project slug: " + slug)
    return slug


def project_path(projects: Path, slug: str, *parts: str) -> Path:
    validate_slug(slug)
    # A symlinked projects root or project can redirect otherwise valid slugs.
    if projects.is_symlink() or projects.resolve() != projects.absolute():
        raise ValueError("projects root must not traverse a symlink")
    project = projects / slug
    target = project.joinpath(*parts)
    if project.resolve() != project.absolute() or not target.resolve().is_relative_to(project.resolve()):
        raise ValueError("project path escapes its directory")
    if any(part in PII_DENY for part in target.relative_to(projects).parts):
        raise ValueError("refusing PII path")
    return target


def pointer_slug(text):
    headings = re.findall(r"^## ACTIVE: (.*)$", text, re.M)
    if len(headings) != 1:
        raise ValueError("pointer must have exactly one ACTIVE block")
    if headings[0] == "(none)":
        return None
    match = re.match(r"`([^`]+)`(?: \(set \d{4}-\d{2}-\d{2}\))?$", headings[0])
    if not match:
        raise ValueError("malformed ACTIVE project slug")
    slug = validate_slug(match.group(1))
    field = re.search(r"^\s*-?\s*\*{0,2}Slug\*{0,2}\s*:\s*`?([^`\n]+?)`?\s*$", text, re.M | re.I)
    if not field or field.group(1) != slug:
        raise ValueError("Slug field and ACTIVE header must identify the same project")
    return slug
