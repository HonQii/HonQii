import feedparser
import json
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()


TOKEN = os.environ.get("GIT_API_TOKEN", "")


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)
    


def fetch_blog_entries():
    entries = feedparser.parse("https://blog.honqi.ink/atom.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]


if __name__ == "__main__":
    readme = root / "README.md"

    readme_contents = readme.open().read()
    rewritten = readme_contents

    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* <a href='{url}' target='_blank'>{title}</a> - {published}".format(**entry) for entry in entries]
    )

    rewritten = replace_chunk(rewritten, "blog", entries_md)

    readme.open("w").write(rewritten)
