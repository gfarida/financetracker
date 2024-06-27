import os
import glob
import shutil


SPHINXAPIDOC = 'sphinx-apidoc'
SOURCEDIR = 'source'
BUILDDIR = 'build'
COVERAGE_DIR = 'htmlcov'
PODEST = 'messages'


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
        os.system(f'{SPHINXAPIDOC} -o ./{SOURCEDIR} ../')
        os.system('make html')
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


def task_pot():
    """Re-create .pot files."""
    return {
        'actions': ['pybabel extract -o messages/messages.pot .'],
        'file_dep': glob.glob('*.py'),
        'targets': ['messages/messages.pot'],
        'clean': True,
    }

def task_po():
    """Update translations."""
    return {
        'actions': ['pybabel update -i messages/messages.pot -d messages'],
        'file_dep': ['messages/messages.pot'],
        'targets': ['messages/ru/LC_MESSAGES/messages.po'],
    }

def task_mo():
    """Compile translations."""
    def create_folder(folder):
        os.makedirs(folder, exist_ok=True)

    return {
        'actions': [
            (create_folder, [f'{PODEST}/ru/LC_MESSAGES']),
            'pybabel compile -d messages'
        ],
        'file_dep': ['messages/ru/LC_MESSAGES/messages.po'],
        'targets': [f'{PODEST}/ru/LC_MESSAGES/messages.mo'],
        'clean': True,
    }

def task_translation():
    """Extract, update, and compile translations."""
    return {
        'actions': None,
        'task_dep': ['pot', 'po', 'mo'],
        'verbosity': 2,
    }


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
