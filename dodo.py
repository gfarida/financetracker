import os
import shutil
import subprocess

SPHINXBUILD = 'sphinx-build'
SOURCEDIR = 'source'
BUILDDIR = 'build'
COVERAGE_DIR = 'htmlcov'

def task_build_and_cov_clean():
    """Clean up the build directory and coverage files."""
    def clean():
        if os.path.exists(BUILDDIR):
            shutil.rmtree(BUILDDIR)
        if os.path.exists(COVERAGE_DIR):
            shutil.rmtree(COVERAGE_DIR)
    return {'actions': [clean]}

def task_git_clean():
    """Run 'git clean -fdx' to clean the repository."""
    return {'actions': ['git clean -fdx']}

def task_html():
    """Build HTML documentation."""
    return {
        'actions': ['cd docs', f'{SPHINXBUILD} -b html {SOURCEDIR} {BUILDDIR}/html'],
        'verbosity': 2,
    }

def task_build():
    """Alias for building HTML documentation."""
    return {'actions': None, 'task_dep': ['html']}

def task_coverage():
    """Run tests and generate coverage report."""
    return {
        'actions': [
            'coverage run -m unittest discover tests -v',
            'coverage report -m',
            'coverage html'
        ],
        'verbosity': 2,
    }
