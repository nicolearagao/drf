from django.db import models
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    """Model for Snippets."""
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default="", blank=True)
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default="python", max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, max_length=100, default="friendly")
    owner = models.ForeignKey("auth.User", related_name="snippets", on_delete=models.CASCADE, default="")
    # auth.User(model reference), related_name reverse relationship access user.snippets.all()
    highlighted = models.TextField(default="")

    def save(self, *args, **kwargs):
        """Define code to be highlighted before saving."""
        """
            Use the `pygments` library to create a highlighted HTML
            representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["created"]
