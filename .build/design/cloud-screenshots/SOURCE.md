# Cloud setup screenshots, Appendix section 2

Taken from `qdrant/landing_page` PR #2492 ("Beginners course module 0"),
file `qdrant-landing/content/course/beginners/module-0/qdrant-cloud.md`,
which sources them from
`qdrant-landing/static/docs/gettingstarted/gui-quickstart/`.

Resized to 760 px wide (the notebook's render width) and embedded in
`Appendix/Appendix.ipynb` as base64 PNGs rather than shipped as files: markdown
image paths break when the platform replaces per-lesson symlinks with
copies, and JupyterLab's sanitizer grants `img` the `data:` scheme, so an
embedded screenshot renders in an untrusted notebook while a linked one
would depend on the file layout.

Re-cut them with `.build/design/cloud-screenshots/rebuild.py` if the
Cloud UI changes.
