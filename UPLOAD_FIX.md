# Fix the missing assets error

For an immediate repair, replace app.py in the ROOT of your GitHub repository with this package's app.py and commit. Keep models.py and requirements.txt in the root. The simulations will run even if manual files are missing.

To restore manuals and figures, upload the entire assets folder alongside app.py. The repository path must be assets/manuals.json, not manuals.json and not edc-lab/assets/manuals.json when app.py is at the root. Preserve all files and subfolders.

GitHub upload: open your repository → Add file → Upload files. Drag the extracted assets folder from your computer into the upload area and commit. Do not upload the ZIP itself.

Expected root:
- app.py
- models.py
- requirements.txt
- assets/manuals.json
- assets/syllabus.pdf
- assets/(all other supplied manuals and images)

Streamlit normally redeploys after a commit. If the old error remains, use Manage app → Reboot app.

The reported traceback used Python 3.14. This failure is caused by a missing file, not by the Python version.
