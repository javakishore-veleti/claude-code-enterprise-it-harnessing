"""On-demand skill loading. Skills live next to each domain harness."""

from __future__ import annotations

from pathlib import Path


def discover_skills(skills_dir: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    if not skills_dir.is_dir():
        return found
    for skill_dir in sorted(skills_dir.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_dir.is_dir() or not skill_md.exists():
            continue
        found[skill_dir.name] = _first_description(skill_md)
    return found


def load_skill(skills_dir: Path, name: str) -> str:
    path = (skills_dir / name / "SKILL.md").resolve()
    if skills_dir.resolve() not in path.parents:
        return f"Error: invalid skill name '{name}'"
    if not path.exists():
        return f"Error: skill '{name}' not found"
    return f"=== SKILL: {name} ===\n\n{path.read_text(encoding='utf-8')}\n\n=== END SKILL ==="


def index_text(skills: dict[str, str]) -> str:
    if not skills:
        return "  (none installed)"
    return "\n".join(f"  - {name}: {desc}" for name, desc in skills.items())


def _first_description(path: Path) -> str:
    in_frontmatter = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or not stripped or stripped.startswith("#"):
            continue
        return stripped[:120]
    return "No description"
