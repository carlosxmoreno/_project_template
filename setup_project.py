"""
Project setup script — creates a new project from this template.

Usage:
    python setup_project.py <ProjectName>

    ProjectName : name of the new project (no spaces). A folder with this
                  name will be created under destination_parent (setup_config.yaml).

    No arguments : prints usage and current configuration, then exits.

    If the project already exists, prompts to overwrite setup files only
    (specs, config, pyproject.toml, README, utilities). Source code, data,
    logs and .venv are never touched.

How it works:
    1. Reads setup_config.yaml from the template directory.
    2. Copies the template folder to destination_parent/ProjectName,
       excluding .venv, .git, __pycache__, setup_config.yaml and this script.
    3. Replaces {{PROJECT_NAME}} placeholders in all listed files.
    4. Optionally removes extended spec files (specs_profile: minimum).
    5. Optionally removes ruff config from pyproject.toml (linter: false).
    6. Creates a Python virtual environment (python_env: venv | conda | none).
    7. Optionally initializes a git repository with an initial commit.
    8. Writes a .project_initialized marker to prevent accidental re-runs.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Root directory of this template (where this script lives).
TEMPLATE_DIR = Path(__file__).parent

# Configuration file read before every run. Edit this file to change defaults.
CONFIG_FILE = TEMPLATE_DIR / "setup_config.yaml"

# String replaced in template files with the actual project name.
PLACEHOLDER = "{{PROJECT_NAME}}"

# Hidden marker file written to the project root after a successful setup.
# Its presence tells the script that the project has already been initialized,
# preventing accidental full re-runs and enabling the overwrite flow instead.
MARKER = ".project_initialized"

# ---------------------------------------------------------------------------
# Spec profiles
# ---------------------------------------------------------------------------

# Files included only in the "extended" specs profile.
# When specs_profile is "minimum", these files are deleted after copying.
# Add or remove entries here to adjust what "extended" means.
EXTENDED_SPECS = [
    "specs/05-data-model.md",
    "specs/06-pipelines.md",
    "specs/07-ux-spec.md",
    "specs/08-api-spec.md",
    "specs/09-test-log.md",
    "specs/10-environment.md",
]

# ---------------------------------------------------------------------------
# Placeholder files
# ---------------------------------------------------------------------------

# All template files that contain {{PROJECT_NAME}} and must be processed.
# If you add a new template file with the placeholder, add it here.
# Files not in this list are copied as-is without placeholder replacement.
FILES_WITH_PLACEHOLDER = [
    ".amazonq/rules/dev-rules.md",
    "config/settings.yaml",
    "pyproject.toml",
    "requirements.txt",
    "README.md",
    "specs/00-working-notes.md",
    "specs/01-vision.md",
    "specs/02-requirements.md",
    "specs/03-architecture.md",
    "specs/04-dev-practices.md",
    "specs/05-data-model.md",
    "specs/06-pipelines.md",
    "specs/07-ux-spec.md",
    "specs/08-api-spec.md",
    "specs/09-test-log.md",
    "specs/10-environment.md",
    "utilities/logger.py",
    "utilities/timestamp.py",
    "utilities/api_errors.py",
]

# ---------------------------------------------------------------------------
# Files excluded from the template copy
# ---------------------------------------------------------------------------

# These items are never copied to the destination project.
# - MARKER             : internal setup marker, not part of the project itself.
# - .venv              : virtual environments are created fresh per project, not copied.
# - .git               : the destination gets its own git history.
# - __pycache__        : compiled bytecode, always regenerated.
# - setup_config.yaml  : template-level config, not relevant to the project.
# - setup_project.py   : this script belongs to the template, not the project.
# - README.md          : the template repo README. The project gets _README_template.md renamed to README.md.
# - sample_*           : example spec files in specs/, for reference only.
_COPY_EXCLUDE = {MARKER, ".venv", ".git", "__pycache__", "setup_config.yaml", "setup_project.py", "README.md"}

# Pattern-based exclusions applied recursively inside subdirectories.
# sample_* files live in specs/ and must be excluded from the copy.
_COPY_EXCLUDE_PATTERNS = ("*.pyc", "sample_*")


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config() -> dict:
    """Load setup_config.yaml and return as dict.

    Exits with an error if the file is not found. This file must always
    exist next to setup_project.py in the template directory.
    """
    if not CONFIG_FILE.exists():
        print(f"ERROR: Configuration file not found: {CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def print_usage(config: dict):
    """Print usage instructions and current configuration, then exit.

    Called when the script is run without arguments. Useful to inspect
    the current setup_config.yaml values before running a setup.
    """
    print()
    print("Usage:")
    print("  python setup_project.py <ProjectName>")
    print()
    print("  ProjectName : name of the new project (no spaces).")
    print("                A folder with this name will be created under destination_parent.")
    print()
    print("Current configuration (setup_config.yaml):")
    print(f"  destination_parent    : {config.get('destination_parent')}")
    print(f"  specs_profile         : {config.get('specs_profile')}")
    print(f"  linter                : {config.get('linter')}")
    print(f"  python_env            : {config.get('python_env')}")
    print(f"  python_version        : {config.get('python_version')}")
    print(f"  venv_system_packages  : {config.get('venv_system_packages')}")
    print(f"  git_init              : {config.get('git_init')}")
    print()
    print("Edit setup_config.yaml to change defaults before running.")
    print()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def replace_placeholder(file_path: Path, project_name: str):
    """Replace PLACEHOLDER in a single file with the actual project name.

    Skips the file silently if it does not exist (e.g. extended spec files
    that were already removed by step_extended_specs).
    Only writes the file if the placeholder is actually present, avoiding
    unnecessary disk writes.
    """
    if not file_path.exists():
        return
    content = file_path.read_text(encoding="utf-8")
    if PLACEHOLDER in content:
        file_path.write_text(content.replace(PLACEHOLDER, project_name), encoding="utf-8")


def is_initialized(directory: Path) -> bool:
    """Return True if the directory contains the initialization marker.

    The marker (.project_initialized) is written by mark_initialized() at
    the end of a successful setup. Its presence is used to distinguish:
    - A freshly initialized project (marker present) → offer overwrite flow.
    - A directory that exists but was not set up by this script → warn and confirm.
    """
    return (directory / MARKER).exists()


def mark_initialized(project_dir: Path):
    """Write the initialization marker file to the project root.

    Called at the end of a successful new project setup. The marker is an
    empty file — its presence is all that matters, not its content.
    """
    (project_dir / MARKER).write_text("", encoding="utf-8")


def read_project_name(project_dir: Path) -> str:
    """Read the project name from config/settings.yaml.

    Falls back to the directory name if settings.yaml does not exist or
    does not contain a resolved name (i.e. still has the placeholder).
    Used to display the project name in informational messages.
    """
    settings = project_dir / "config" / "settings.yaml"
    if settings.exists():
        for line in settings.read_text(encoding="utf-8").splitlines():
            if "name:" in line and PLACEHOLDER not in line:
                return line.split("name:")[-1].strip().strip('"')
    return project_dir.name


# ---------------------------------------------------------------------------
# Setup steps
# Each step is a discrete, independently testable action.
# Steps are called in sequence from main() for new projects,
# or selectively for the overwrite flow on existing projects.
# ---------------------------------------------------------------------------

def step_copy_template(project_dir: Path):
    """Copy the template directory to the destination project directory.

    Excludes items in _COPY_EXCLUDE (see constant definition for rationale).
    If the destination already exists (non-initialized directory), copies
    into it with dirs_exist_ok=True to merge without deleting existing files.
    If the destination does not exist, uses shutil.copytree for a clean copy.
    """
    print(f"  Copying template to {project_dir} ...")
    ignore = shutil.ignore_patterns(*_COPY_EXCLUDE, *_COPY_EXCLUDE_PATTERNS)
    if project_dir.exists():
        # Merge into existing directory — does not delete files already there.
        for item in TEMPLATE_DIR.iterdir():
            if item.name in _COPY_EXCLUDE:
                continue
            target = project_dir / item.name
            if item.is_dir():
                shutil.copytree(item, target, ignore=ignore, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target)
    else:
        shutil.copytree(TEMPLATE_DIR, project_dir, ignore=ignore)

    # _README_template.md is the project README template (contains {{PROJECT_NAME}}).
    # It is copied as-is by copytree, then renamed to README.md in the destination.
    # The template's own README.md (repo-level) is excluded from the copy.
    readme_template = project_dir / "_README_template.md"
    readme_dest = project_dir / "README.md"
    if readme_template.exists():
        readme_template.rename(readme_dest)
    print("  Done.")


def step_replace_placeholders(project_dir: Path, project_name: str):
    """Replace {{PROJECT_NAME}} in all FILES_WITH_PLACEHOLDER.

    Iterates over the full list and calls replace_placeholder() on each.
    Files that do not exist (e.g. extended specs removed earlier) are
    skipped silently inside replace_placeholder().
    """
    print("  Replacing placeholders ...")
    for relative in FILES_WITH_PLACEHOLDER:
        replace_placeholder(project_dir / relative, project_name)
    print("  Done.")


def step_copy_missing_files(project_dir: Path):
    """Copy FILES_WITH_PLACEHOLDER entries missing from an existing project.

    Used in the overwrite flow when the user changes specs_profile from
    minimum to extended: the extended spec files do not exist in the project
    yet and must be copied from the template before placeholder replacement.
    Only copies files that are absent — never overwrites existing content.

    Special case: README.md in the destination comes from _README_template.md
    in the template (the template's own README.md is the repo-level README and
    is excluded from the copy).
    """
    for relative in FILES_WITH_PLACEHOLDER:
        dest = project_dir / relative
        if not dest.exists():
            # README.md in the destination is sourced from _README_template.md.
            src = TEMPLATE_DIR / ("_README_template.md" if relative == "README.md" else relative)
            if src.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)


def step_extended_specs(project_dir: Path, keep: bool, verbose: bool = True):
    """Remove extended spec files when specs_profile is 'minimum'.

    When keep=False, deletes the files listed in EXTENDED_SPECS if they exist.
    Only prints output if verbose=True. verbose=False is used during new project
    creation (the user already confirmed the profile in the summary screen).

    WARNING: if these files contain content written by the developer, it will
    be permanently deleted. This is intentional when downgrading from extended
    to minimum, but should be done with care.
    """
    if not keep:
        to_remove = [project_dir / r for r in EXTENDED_SPECS if (project_dir / r).exists()]
        if to_remove:
            if verbose:
                print("  Removing extended specs ...")
            for path in to_remove:
                path.unlink()
            if verbose:
                print("  Done.")


def step_linter(project_dir: Path, keep: bool, verbose: bool = True):
    """Remove the ruff configuration block from pyproject.toml if linter=false.

    When keep=False, strips all [tool.ruff*] sections from pyproject.toml.
    The removal is line-based: once a [tool.ruff line is found, lines are
    dropped until the next blank line that follows a non-blank line, which
    signals the end of the section.

    verbose=False suppresses output during new project creation (same rationale
    as step_extended_specs).

    WARNING: if the developer has manually customized the ruff section,
    those changes will be lost when switching linter from true to false.
    """
    if not keep:
        if verbose:
            print("  Removing ruff configuration ...")
        pyproject = project_dir / "pyproject.toml"
        if pyproject.exists():
            lines = pyproject.read_text(encoding="utf-8").splitlines()
            filtered = []
            skip = False
            for line in lines:
                if line.startswith("[tool.ruff"):
                    skip = True
                if not skip:
                    filtered.append(line)
                elif line == "" and filtered and filtered[-1] != "":
                    skip = False
            pyproject.write_text("\n".join(filtered), encoding="utf-8")
        if verbose:
            print("  Done.")


def step_python_env(project_dir: Path, env_type: str, python_version: str, system_packages: bool = False):
    """Create the Python virtual environment for the project.

    Supports three modes controlled by python_env in setup_config.yaml:

    - venv   : creates a standard .venv inside the project directory using
               the Python interpreter that runs this script (sys.executable).
               If venv_system_packages is true, the venv is created with
               --system-site-packages, which makes all packages installed in
               the system Python visible inside the venv without reinstalling
               them. This saves significant disk space when multiple projects
               share the same dependencies (e.g. pyyaml, requests, pydantic).
               Trade-off: less isolation — system package versions are visible
               and can interfere with project-specific pins in requirements.txt.

    - conda  : creates a named conda environment using the project directory
               name as the environment name. Requires conda to be installed
               and available on PATH. python_version is used here.

    - none   : skips environment creation entirely. Use this when you manage
               environments externally (pyenv, global conda, uv, etc.) or
               when you want to set up the environment manually after setup.

    Args:
        project_dir     : root directory of the new project.
        env_type        : "venv" | "conda" | "none".
        python_version  : Python version string, e.g. "3.11". Used by conda only.
        system_packages : if True and env_type is "venv", passes
                          --system-site-packages to venv. Default False.
    """
    if env_type == "none":
        # No environment created. The developer is responsible for setting
        # up their own environment before installing requirements.txt.
        return

    if env_type == "venv":
        venv_path = project_dir / ".venv"
        print(f"  Creating venv at {venv_path} ...")

        cmd = [sys.executable, "-m", "venv", str(venv_path)]
        if system_packages:
            # --system-site-packages: the venv can see packages installed in
            # the base Python. Avoids duplicating large packages (numpy, torch,
            # pydantic, etc.) across every project. Set venv_system_packages: true
            # in setup_config.yaml to enable this.
            cmd.append("--system-site-packages")

        subprocess.run(cmd, check=True)
        print("  Done.")
        if sys.platform == "win32":
            print("  Activate with: .venv\\Scripts\\activate")
        else:
            print("  Activate with: source .venv/bin/activate")

    elif env_type == "conda":
        # Creates a named conda environment. The environment name matches the
        # project directory name so it is easy to identify in `conda env list`.
        env_name = project_dir.name
        print(f"  Creating conda environment '{env_name}' (Python {python_version}) ...")
        subprocess.run(
            ["conda", "create", "-n", env_name, f"python={python_version}", "-y"],
            check=True,
        )
        print(f"  Done. Activate with: conda activate {env_name}")


def step_git(project_dir: Path):
    """Initialize a git repository and create the initial commit.

    Runs git init, stages all files, and commits with a conventional commit
    message. The .gitignore in the template already excludes .venv, __pycache__,
    .env and other files that should not be tracked.

    After setup, connect to a remote repository manually:
      1. Create an empty repository on GitHub (or other host).
      2. git remote add origin <repo_url>
      3. git push -u origin main
    """
    print("  Initializing git repository ...")
    subprocess.run(["git", "init"], cwd=project_dir, check=True)
    subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
    subprocess.run(
        ["git", "commit", "-m", "feat: initial project structure from template"],
        cwd=project_dir,
        check=True,
    )
    print("  Done.")
    print()
    print("  To connect to GitHub:")
    print("  1. Create an empty repository on https://github.com")
    print("  2. git remote add origin <repo_url>")
    print("  3. git push -u origin main")


# ---------------------------------------------------------------------------
# Overwrite warning
# ---------------------------------------------------------------------------

def show_overwrite_warning(config: dict, project_dir: Path):
    """Print a detailed warning before overwriting an existing project's setup files.

    Called when the destination project already exists and has been initialized.
    Lists exactly what will and will not be touched, and highlights the risks
    of each type of change so the user can make an informed decision.
    """
    print()
    print("=" * 50)
    print("  WARNING: project already exists")
    print("=" * 50)
    print(f"  Directory : {project_dir}")
    print()
    print("  Only FILES_WITH_PLACEHOLDER will be overwritten (specs, config,")
    print("  pyproject.toml, README, utilities, etc.).")
    print("  Source code, data, logs and .venv will NOT be touched.")
    print()
    print("  Risks depending on what changed in setup_config.yaml:")
    print("  - specs_profile extended -> minimum : spec files with content will be deleted.")
    print("  - linter true -> false              : custom ruff config in pyproject.toml will be lost.")
    print("  - Any change                        : manually edited placeholder files will be overwritten.")
    print()
    print("  Changing the project name is NOT recommended.")
    print("  There is no automatic backup. Make a manual copy if needed.")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Entry point. Orchestrates the full setup flow.

    Flow for a new project:
        1. Load config.
        2. Parse project name from CLI argument.
        3. If destination exists and is initialized → overwrite flow.
        4. If destination exists but is not initialized → warn and confirm.
        5. Show summary and ask for confirmation.
        6. Run all setup steps in order.
        7. Write initialization marker.

    Flow for an existing initialized project (overwrite):
        1. Show warning with risks.
        2. Ask for confirmation.
        3. Copy missing files (e.g. new extended specs).
        4. Replace placeholders.
        5. Apply specs profile and linter settings.
        6. Exit (no venv or git changes).
    """
    config = load_config()

    # No arguments: print usage and current config, then exit.
    # This is a safe read-only mode — nothing is created or modified.
    if len(sys.argv) < 2:
        print_usage(config)
        sys.exit(0)

    project_name = sys.argv[1]
    if " " in project_name:
        print("ERROR: Project name cannot contain spaces.")
        sys.exit(1)

    # Resolve all config values with sensible defaults.
    destination_parent = Path(config["destination_parent"])
    project_dir = destination_parent / project_name
    specs_profile = config.get("specs_profile", "minimum")
    linter = config.get("linter", True)
    python_env = config.get("python_env", "venv")
    python_version = config.get("python_version", "3.11")
    # venv_system_packages: expose system-installed packages inside the venv.
    # Saves disk space at the cost of reduced isolation. See step_python_env().
    venv_system_packages = config.get("venv_system_packages", False)
    git_init = config.get("git_init", True)

    # --- Overwrite flow: project exists and was previously initialized ---
    # Only setup files (FILES_WITH_PLACEHOLDER) are updated.
    # Source code, data, logs and .venv are never touched in this flow.
    if project_dir.exists() and is_initialized(project_dir):
        show_overwrite_warning(config, project_dir)
        confirm = input("Overwrite setup files in existing project? [y/N]: ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Aborted.")
            sys.exit(0)
        print()
        # Copy files that may be new (e.g. extended specs not present before).
        step_copy_missing_files(project_dir)
        step_replace_placeholders(project_dir, project_name)
        step_extended_specs(project_dir, keep=(specs_profile == "extended"))
        step_linter(project_dir, keep=linter)
        print()
        print("=" * 50)
        print(f"  Setup files updated in '{project_name}'.")
        print("=" * 50)
        sys.exit(0)

    # --- Destination exists but was not initialized by this script ---
    # Could be a manually created directory or a partial setup. Warn and confirm
    # before merging the template into it.
    elif project_dir.exists():
        print(f"WARNING: Destination directory already exists: {project_dir}")
        confirm = input("It will be overwritten. Proceed? [y/N]: ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Aborted.")
            sys.exit(0)

    # --- New project: show summary and ask for confirmation ---
    print()
    print("=" * 50)
    print("  New project summary")
    print("=" * 50)
    print(f"  Name                  : {project_name}")
    print(f"  Destination           : {project_dir}")
    print(f"  Specs profile         : {specs_profile}")
    print(f"  Linter (ruff)         : {linter}")
    print(f"  Python env            : {python_env} (Python {python_version})")
    print(f"  venv system packages  : {venv_system_packages}")
    print(f"  Git init              : {git_init}")
    print()

    confirm = input("Proceed? [Y/n]: ").strip().lower()
    if confirm not in ("", "y", "yes"):
        print("Aborted.")
        sys.exit(0)

    # --- Run all setup steps ---
    print()
    step_copy_template(project_dir)
    step_replace_placeholders(project_dir, project_name)
    # verbose=False: the user already saw and confirmed the profile in the summary.
    step_extended_specs(project_dir, keep=(specs_profile == "extended"), verbose=False)
    step_linter(project_dir, keep=linter, verbose=False)
    step_python_env(project_dir, python_env, python_version, system_packages=venv_system_packages)
    if git_init:
        step_git(project_dir)

    # Write the marker so future runs detect this as an initialized project.
    mark_initialized(project_dir)

    print()
    print("=" * 50)
    print(f"  Project '{project_name}' is ready.")
    print(f"  {project_dir}")
    print("  Next: fill in specs/01-vision.md to start.")
    print("=" * 50)


if __name__ == "__main__":
    main()
