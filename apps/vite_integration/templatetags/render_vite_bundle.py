# This template tag is needed for production
# Add it to one of your django apps (/appdir/templatetags/render_vite_bundle.py, for example)

import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_vite_bundle():
    """
    Template tag to render a vite bundle.
    Supposed to only be used in production.
    For development, see other files.
    """

    try:
        fd = open(f"{settings.FRONTEND_BUILD_DIR}/.vite/manifest.json", "r")
        manifest = json.load(fd)
    except Exception:
        raise Exception(
            f"Vite manifest file not found or invalid. Maybe your {settings.FRONTEND_BUILD_DIR}/.vite/manifest.json file is empty?"
        )
    if 'imports' in manifest["index.html"]:

        imports_files = "".join(
            [
                f'<script type="module" src="/static/{manifest[file]["file"]}"></script>'
                for file in manifest["index.html"]["imports"]
            ]
        )
    else:
        imports_files = ''
    
    if "css" in manifest["index.html"]:
        css_file = f"""<link rel="stylesheet" type="text/css" href="/static/{manifest['index.html']['css'][0]}" />"""
    else:
        css_file = ''

    return mark_safe(
        f"""<script type="module" src="/static/{manifest['index.html']['file']}"></script>
        {css_file}
        {imports_files}"""
    )
