import logging

import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if not info:
            logging.debug("Rendering code block without language")
            return f"\n<pre><code>{mistune.escape(code)}</code></pre>\n"

        try:
            lexer = get_lexer_by_name(info, stripall=True)
            formatter = html.HtmlFormatter()
            logging.debug(f"Rendering code block with language: {info}")
            return highlight(code, lexer, formatter)
        except Exception as e:
            logging.warning(f"Failed to highlight code block for language '{info}': {e}")
            return f"\n<pre><code>{mistune.escape(code)}</code></pre>\n"
