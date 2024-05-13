import subprocess

def get_git_revision_short_hash() -> str:
    """Get the short hash of the current git commit."""
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    except:
        return "not_available"

def get_git_path_hash(path) -> str:
    """Get the short hash of the last commit in which the path or a sub path was modified."""
    try:
        return subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:%h', path]).decode('ascii').strip()
    except:
        return "not_available"

def is_git_available():
    """Check whether `git` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    try:
        return which("git") is not None
    except:
        return False
