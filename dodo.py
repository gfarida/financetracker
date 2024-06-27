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
    def build_html():
        os.chdir('docs')
        os.system(f'{SPHINXBUILD} -b html {SOURCEDIR} {BUILDDIR}/html')
        os.chdir('..')  # Change back to the original directory

    return {
        'actions': [build_html],
        'targets': [os.path.join('docs', BUILDDIR, 'html')],
        'clean': True,
        'verbosity': 2,
    }

def task_build():
    """Alias for building HTML documentation."""
    return {'actions': None, 'task_dep': ['html']}

def task_build():
    """Alias for building HTML documentation."""
    return {'actions': None, 'task_dep': ['html']}

def task_coverage():
    """Run tests and generate coverage report."""
    def run_coverage():
        os.system('coverage run -m unittest discover tests -v')
        os.system('coverage report -m')
        os.system('coverage html')

    return {
        'actions': [run_coverage],
        'targets': [COVERAGE_DIR],
        'clean': True,
        'verbosity': 2,
    }

def task_wheel():
    """Build a wheel package."""
    return {
        'actions': ['python3 -m build -w'],
        'verbosity': 2,
    }
