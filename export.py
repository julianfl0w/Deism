import ast
from datetime import date, datetime, UTC
import html as html_lib
import json
import os
import shutil
import sys
from copy import deepcopy
from pathlib import Path
import re

from bs4 import BeautifulSoup as bs


ROOT_DIR = Path(__file__).resolve().parent
BOOK_DIR = ROOT_DIR / "Book Of Doctrine"
SRC_DIR = ROOT_DIR / "src"
BUILD_DIR = ROOT_DIR / "build"
GRAPHS_DIR_NAME = "graphs"
BASE_URL_PREFIX = ""
SITE_URL = os.environ.get("SITE_URL", "https://deism.church").rstrip("/")
ASSET_VERSION = os.environ.get("ASSET_VERSION", datetime.now(UTC).strftime("%Y%m%d%H%M%S"))

LINE_COLOR = '"#88ffff"'

DEFAULT_META = {
    "priority": 1000,
    "ignore": False,
    "type": "default",
    "topology": "nested",
    "noPropagate": {},
    "font": {"color": "white"},
    "relationship": "descends",
    "engine": "dot",
    "graphParams": {
        "rankdir": "TB",
        "style": "filled",
        "fontcolor": "black",
        "color": "black",
        "bgcolor": "white",
        "gradientangle": 0,
        "dpi": 300,
    },
    "boxParams": {
        "rankdir": "TB",
        "shape": "box",
        "penwidth": 1,
        "color": LINE_COLOR,
        "fontcolor": "black",
        "fillcolor": "white",
        "style": "filled",
        "gradientangle": 270.05,
    },
    "arrowParams": {"color": LINE_COLOR, "penwidth": 1},
}

SPECIAL_NODE_NAMES = {
    "Recognized_Theologians": "Personal",
}


def depth_first_dict_merge(priority, additions):
    if isinstance(priority, dict):
        retval = deepcopy(priority)
        for key, value in additions.items():
            if key in retval:
                retval[key] = depth_first_dict_merge(retval[key], value)
            else:
                retval[key] = deepcopy(value)
        return retval
    if isinstance(priority, list):
        return priority + additions
    return priority


def load_python_data(path, extra_globals=None):
    source = path.read_text(encoding="utf-8")
    module = ast.parse(source, filename=str(path))
    globals_dict = {"__file__": str(path)}
    if extra_globals:
        globals_dict.update(extra_globals)

    if module.body and isinstance(module.body[-1], ast.Expr):
        body = module.body[:-1]
        if body:
            exec(
                compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"),
                globals_dict,
            )
        expr = module.body[-1].value
        return eval(compile(ast.Expression(expr), str(path), "eval"), globals_dict)

    exec(compile(module, str(path), "exec"), globals_dict)
    for key in ("DATA", "GRAPH", "CONTENT"):
        if key in globals_dict:
            return globals_dict[key]

    assigned_data = {}
    for statement in module.body:
        if not isinstance(statement, ast.Assign):
            continue
        for target in statement.targets:
            if not isinstance(target, ast.Name):
                continue
            name = target.id
            if name.startswith("_") or name not in globals_dict:
                continue
            value = globals_dict[name]
            if isinstance(value, dict):
                assigned_data[display_name_from_symbol(name, path.stem)] = value

    if assigned_data:
        return assigned_data

    raise ValueError(f"No data expression or DATA/GRAPH/CONTENT in {path}")


def display_name_from_symbol(symbol, module_name):
    if symbol in SPECIAL_NODE_NAMES:
        return SPECIAL_NODE_NAMES[symbol]

    suffix = f"_{module_name}"
    if symbol.endswith(suffix):
        symbol = symbol[: -len(suffix)]

    return symbol.replace("_", " ")


def create_node(name, parent, depth, context):
    if parent is None:
        meta = deepcopy(DEFAULT_META)
    else:
        meta = {}
        parent_meta = parent.get("meta", {})
        no_propagate = parent_meta.get("noPropagate", {}) or {}
        for key, value in parent_meta.items():
            if key in no_propagate:
                continue
            meta[key] = deepcopy(value)

    node = {
        "name": name,
        "children": [],
        "parent": parent,
        "depth": depth,
        "meta": meta,
        "origin": None,
        "explicitPriority": False,
        "sourceOrder": context["nodeNumber"],
        "clusterName": f"\"cluster_{context['nodeNumber']}\"",
    }
    context["nodeNumber"] += 1
    return node


def apply_meta(node, meta):
    if "priority" in meta:
        node["explicitPriority"] = True
    node["meta"] = depth_first_dict_merge(meta, node["meta"])


def process_text(node, source, context):
    if isinstance(source, list):
        for element in source:
            child = create_node("", node, node["depth"] + 1, context)
            child["origin"] = "text"
            node["children"].append(child)
            process_text(child, element, context)
        node["meta"] = depth_first_dict_merge({"type": "list"}, node["meta"])
        return

    if isinstance(source, dict):
        for key, value in source.items():
            if key == "meta":
                apply_meta(node, value)
                continue
            child = create_node(key, node, node["depth"] + 1, context)
            child["origin"] = "text"
            node["children"].append(child)
            process_text(child, value, context)
        return

    if source is not None:
        node["name"] = source


def build_from_file(path, parent, depth, context):
    node = create_node(path.stem, parent, depth, context)
    node["origin"] = "file"
    source = load_python_data(path)
    process_text(node, source, context)
    promote_priority_from_children(node)
    if parent is not None:
        parent["children"].append(node)
    return node


def build_from_directory(path, parent, depth, context):
    node = create_node(path.name, parent, depth, context)
    node["origin"] = "directory"
    if parent is not None:
        parent["children"].append(node)

    for entry_name in os.listdir(path):
        resolved = path / entry_name
        if entry_name == "meta.py":
            apply_meta(node, load_python_data(resolved))
            continue

        if resolved.is_dir():
            if entry_name in {"graphs", "__pycache__"}:
                continue
            build_from_directory(resolved, node, depth + 1, context)
            continue

        if resolved.suffix == ".py":
            if entry_name.startswith("_") or entry_name == "json2html.py":
                continue
            build_from_file(resolved, node, depth + 1, context)

    if parent is not None:
        promote_priority_from_children(node)
    return node


def promote_priority_from_children(node):
    if node["explicitPriority"]:
        return

    child_priorities = [
        child["meta"].get("priority", 1000)
        for child in node["children"]
        if child.get("explicitPriority")
    ]
    if not child_priorities:
        return

    node["meta"]["priority"] = min(child_priorities)


def compute_height_no_lists(node):
    for child in node["children"]:
        compute_height_no_lists(child)

    if not node["children"] or node["meta"].get("type") != "default":
        node["_maxheight"] = 0
        node["_minheight"] = 0
    else:
        node["_maxheight"] = 1 + max(c["_maxheight"] for c in node["children"])
        node["_minheight"] = 1 + min(c["_maxheight"] for c in node["children"])
    return node["_maxheight"]


def sort_children_by_priority(node):
    for child in node["children"]:
        sort_children_by_priority(child)
    node["children"].sort(
        key=lambda c: (c["meta"].get("priority", 1000), c.get("sourceOrder", 0))
    )


def get_ancestors(node):
    if node["parent"] is None:
        return [node]
    return get_ancestors(node["parent"]) + [node]


def slugify(value):
    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "untitled"


def public_url(*parts):
    path = "/".join(slugify(part) for part in parts if str(part).strip())
    return "/" + path if path else "/"


def gen_url(node):
    ancestors = get_ancestors(node)
    node["urlDir"] = public_url(*[a["name"] for a in ancestors[:-1]])
    node["urlPath"] = os.path.join(
        ".", *[slugify(a["name"]) for a in ancestors[:-1]]
    )
    base = "" if node["urlDir"] == "/" else node["urlDir"]
    node["url"] = f"{base}/{slugify(node['name'])}.html"
    node["path"] = os.path.join(
        node["urlPath"], slugify(node["name"]) + ".html"
    )
    if node["parent"] is None:
        node["url"] = "/book_of_doctrine/"
        node["path"] = os.path.join("book_of_doctrine", "index.html")
    return node["url"]


def asset_prefix(node):
    gen_url(node)
    parent = Path(node["path"]).parent
    if str(parent) == ".":
        return ""
    parts = [p for p in parent.parts if p not in (".", "")]
    return "../" * len(parts)


def get_elder_sibling(node):
    if not node["parent"]:
        return node
    index = node["parent"]["children"].index(node)
    return node["parent"]["children"][index - 1]


def get_younger_sibling(node):
    if not node["parent"]:
        return node
    siblings = node["parent"]["children"]
    index = siblings.index(node)
    return siblings[(index + 1) % len(siblings)]


def get_apex(node):
    while node["parent"] is not None:
        node = node["parent"]
    return node


def from_above(node, key):
    curr = node
    while curr is not None:
        if key in curr:
            return curr[key]
        curr = curr["parent"]
    raise KeyError(f"Key {key} not found above")


def add_verse_no(node):
    markdown_string = ""
    html_string = ""
    apex = get_apex(node)
    if apex.get("displayVerseNo"):
        verse_no = apex["verseNo"]
        markdown_string += "<sup>" + str(verse_no) + "</sup> "
        html_string += "<sup>" + str(verse_no) + "</sup> "
        apex["verseNo"] += 1
    return {"html": html_string, "markdown": markdown_string}


def get_reference_superscript(node):
    markdown_string = ""
    html_string = ""
    apex = get_apex(node)

    if "reference" in node["meta"]:
        for reference in node["meta"]["reference"]:
            reference_no = apex["referenceNo"]
            reference_letter = f"{reference_no}"
            apex["referenceNo"] += 1
            markdown_string += (
                "<sup>[" + reference_letter + "](" + reference + ")</sup> "
            )
            html_string += (
                "<sup><a href=" + reference + ">" + reference_letter + "</a></sup> "
            )

    return {"html": html_string, "markdown": markdown_string}


def flatten(node):
    toret = [node]
    for child in node["children"]:
        toret += flatten(child)
    return toret


def preformat_list_recurse(node, depth=0):
    if not node["children"]:
        return node["name"]
    text_string = ""
    for i, child in enumerate(node["children"]):
        text_string += preformat_list_recurse(child, depth=depth + 1)
        if i < len(node["children"]) - 1:
            text_string += ", "
    return text_string


def list_recurse(node, relationship="contains", depth=0):
    if not node["children"]:
        return node["name"]
    text_string = ""
    if depth > 0:
        text_string += f"{node['name']}, which {relationship}"
    else:
        text_string += f"{node['name']}, {relationship} "
    for i, child in enumerate(node["children"]):
        if i == len(node["children"]) and "and" not in node["name"].lower():
            text_string += ", and "
        text_string += list_recurse(child, relationship=relationship, depth=depth + 1)
        text_string += "\n"
    return text_string


def to_list(node, depth=0):
    markdown_string = "  " * depth + "- " + node["name"] + "\n"
    for child in node["children"]:
        markdown_string += to_list(child, depth=depth + 1)["markdown"]

    html_string = "<li>\n" + node["name"]
    reference_superscript = get_reference_superscript(node)
    html_string += reference_superscript["html"]
    markdown_string += reference_superscript["markdown"]

    if node["children"]:
        html_string += "<ol>\n"
        for child in node["children"]:
            html_string += to_list(child, depth=depth + 1)["html"]
        html_string += "</ol>\n"
    html_string += "</li>"
    return {"html": html_string, "markdown": markdown_string}


def to_table_of_contents(node, minHeight=0, maxDepth=-1):
    markdown_string = ""
    html_string = ""

    if "tableOfContentsSkip" in node["meta"]:
        return {"html": html_string, "markdown": markdown_string}

    if node["depth"] > maxDepth and maxDepth >= 0:
        return {"html": html_string, "markdown": markdown_string}

    if node["_maxheight"] < minHeight:
        return {"html": html_string, "markdown": markdown_string}

    markdown_string += "  " * node["depth"] + "- " + node["name"] + "\n"
    for child in node["children"]:
        markdown_string += to_table_of_contents(
            child, minHeight=minHeight, maxDepth=maxDepth
        )["markdown"]

    html_string += "<li>\n"
    apex = get_apex(node)
    if "link" in apex:
        html_string += (
            "<a href=#" + node["name"].replace(" ", "_") + ">" + node["name"] + "</a>"
        )
    else:
        html_string += node["name"]

    if node["children"]:
        html_string += "<ol>\n"
        for child in node["children"]:
            html_string += to_table_of_contents(
                child, minHeight=minHeight, maxDepth=maxDepth
            )["html"]
        html_string += "</ol>\n"
    html_string += "</li>"
    return {"html": html_string, "markdown": markdown_string}


def as_dot_notation(node, start_depth):
    dot_notation = ""
    if node["meta"].get("ignore"):
        return dot_notation

    node["boxLabel"] = '"' + node["name"] + '"'
    node["meta"]["boxParams"]["label"] = node["boxLabel"]

    box_params_string = " ["
    box_params_flat = ""
    for key, value in node["meta"]["boxParams"].items():
        box_params_string += key + "=" + str(value) + ", "
        box_params_flat += key + "=" + str(value) + ";\n "
    box_params_string = box_params_string[:-2] + "]\n"

    if not any(c["meta"].get("relationship") == "within" for c in node["children"]):
        dot_notation += node["clusterName"] + box_params_string

    if "maxDepth" not in node["meta"] or (node["depth"] - start_depth) < node["meta"]["maxDepth"]:
        if any(c["meta"].get("relationship") == "within" for c in node["children"]):
            dot_notation += "subgraph " + node["clusterName"] + "{\n"
            dot_notation += box_params_flat
            for child in node["children"]:
                if child["meta"].get("relationship") == "within":
                    dot_notation += as_dot_notation(child, start_depth=start_depth)
            dot_notation += "}\n"

        for child in node["children"]:
            if child["meta"].get("relationship") == "descends":
                child["meta"]["arrowParams"]["ltail"] = node["clusterName"]
                child["meta"]["arrowParams"]["lhead"] = child["clusterName"]

                dot_notation += as_dot_notation(child, start_depth=start_depth)
                dot_notation += node["clusterName"] + " -> " + child["clusterName"] + " ["
                for key, value in child["meta"]["arrowParams"].items():
                    dot_notation += key + "=" + str(value) + ", "
                dot_notation = dot_notation[:-2] + "]\n"

    return dot_notation


def to_graphviz(node, prefix):
    dot_string = "digraph D {\n"
    for key, value in node["meta"]["graphParams"].items():
        dot_string += key + " = " + str(value) + "\n"

    for child in node["children"]:
        dot_string += as_dot_notation(child, start_depth=child["depth"])
    dot_string += "}"

    apex = get_apex(node)
    node["imageName"] = os.path.join(
        apex["graphsDir"], node["name"].replace(" ", "_") + ".png"
    )

    if not apex.get("skipGraphs"):
        engine = node["meta"]["engine"]
        if shutil.which(engine) is None:
            apex["skipGraphs"] = True
        else:
            build_graph_dir = os.path.join(apex["buildDir"], apex["graphsDir"])
            os.makedirs(build_graph_dir, exist_ok=True)
            dot_filename = os.path.join(build_graph_dir, node["name"].replace(" ", "_") + ".dot")
            with open(dot_filename, "w+", encoding="utf-8") as f:
                f.write(dot_string)
            node["buildImageName"] = os.path.join(apex["buildDir"], node["imageName"])
            runstring = f"{engine} -Tpng {dot_filename} -o '{node['buildImageName']}'"
            os.system(runstring)

    if apex.get("skipGraphs"):
        return {"html": "", "markdown": ""}

    markdown_string = (
        node["name"]
        + "\n"
        + ("\n![" + node["name"] + "](" + prefix + node["imageName"] + "?raw=true)\n\n")
    )
    html_string = (
        "<br>"
        + '<figure><img src="'
        + prefix
        + node["imageName"]
        + f'" width="100%"><figcaption>{node["name"]}</figcaption></figure>\n'
    )
    return {"html": html_string, "markdown": markdown_string}


def eval_command(node, command):
    if command.startswith("self.getApex().toTableOfContents"):
        match = re.search(r"toTableOfContents\\((.*)\\)", command)
        kwargs = {}
        if match:
            args = match.group(1).strip()
            if args:
                for part in args.split(","):
                    key, value = part.split("=")
                    kwargs[key.strip()] = int(value)
        return to_table_of_contents(get_apex(node), **kwargs)
    raise ValueError(f"Unsupported eval command: {command}")


def to_markdown(node):
    markdown_string = ""
    html_string = ""
    text_string = ""

    if node["meta"].get("ignore"):
        return {"html": html_string, "markdown": markdown_string, "text": text_string}

    if node["depth"] == 0:
        html_string += "<html>\n"
        html_string += (
            f'<body style="color: {from_above(node, "textColor")} ;align:{from_above(node, "align")}">\n'
        )

    node_type = node["meta"].get("type")
    if node_type == "lineage":
        prefix = asset_prefix(node)
        markdown_string += "\n"
        html_string += "\n"
        gv = to_graphviz(node, prefix)
        markdown_string += gv["markdown"]
        html_string += gv["html"]
        text_string += f"Here is our {node['name']}. "
        for child in node["children"]:
            text_string += list_recurse(child, depth=0)

    elif node_type == "prompt":
        html_string += "<i>"
        html_string += '<ol style="list-style: none;padding-left: 0;">'

        reference_superscript = get_reference_superscript(node)
        html_string += reference_superscript["html"]
        markdown_string += reference_superscript["markdown"]

        text_string += preformat_list_recurse(node)
        html_string += "</i>"
        markdown_string += "\n\n"
        html_string += "\n\n"

    elif node_type == "list":
        verse_superscript = add_verse_no(node)
        html_string += verse_superscript["html"] + node["name"] + "\n"
        markdown_string += verse_superscript["markdown"] + node["name"] + "\n"
        text_string += node["name"] + "\n"

        if node["meta"].get("topology") != "flat":
            html_string += "<ol>"

        if node["meta"].get("topology") == "flat":
            html_string += "<ol>\n"
            for child in flatten(node)[1:]:
                html_string += "<li>" + child["name"] + "</li>\n"
                markdown_string += "- " + child["name"] + "\n"
            html_string += "</ol>\n"
        else:
            for child in node["children"]:
                child_mark = to_list(child, depth=0)
                markdown_string += child_mark["markdown"]
                html_string += child_mark["html"]
            html_string += "</ol>"

        reference_superscript = get_reference_superscript(node)
        html_string += reference_superscript["html"]
        markdown_string += reference_superscript["markdown"]
        text_string += preformat_list_recurse(node)
        markdown_string += "\n\n"
        html_string += "\n\n"

    elif node_type == "eval":
        out = eval_command(node, node["meta"]["command"])
        markdown_string += out["markdown"] + "\n"
        html_string += out["html"] + "\n"

    elif node_type == "wisdom":
        verse_superscript = add_verse_no(node)
        reference_superscript = get_reference_superscript(node)
        html_string += verse_superscript["html"] + str(node["name"]) + reference_superscript["html"]
        markdown_string += (
            verse_superscript["markdown"]
            + str(node["name"])
            + reference_superscript["markdown"]
        )

        if markdown_string[-1] not in [".", "!", ":", ",", ">", "?", "\n"]:
            html_string += ". "
            markdown_string += ". "

        html_string += "<br>"
        markdown_string += "\n\n"

    elif node_type == "default":
        if node["_maxheight"] == 0:
            verse_superscript = add_verse_no(node)
            reference_superscript = get_reference_superscript(node)
            text_string += str(node["name"]).replace("<br>", "")
            html_string += (
                verse_superscript["html"]
                + str(node["name"])
                + reference_superscript["html"]
            )
            markdown_string += (
                verse_superscript["markdown"]
                + str(node["name"])
                + reference_superscript["markdown"]
            )

            if markdown_string[-1] not in [".", "!", ":", ",", ">", "?", "\n"]:
                html_string += ". "
                markdown_string += ". "
        else:
            markdown_string += "\n"
            markdown_string += "#" * (node["depth"]) + " " + node["name"] + "\n\n"
            if node["depth"] == 0:
                html_string += "<title>" + node["name"] + "</title>\n"
            gen_url(node)
            html_string += (
                "<h"
                + str(node["depth"] + 1)
                + ">"
                + "<a href="
                + node["url"]
                + ">"
                + node["name"]
                + "</a>"
                + "</h"
                + str(node["depth"] + 1)
                + ">\n"
            )
            get_apex(node)["verseNo"] = 0

        for child in node["children"]:
            child_mark = to_markdown(child)
            markdown_string += child_mark["markdown"]
            html_string += child_mark["html"]

        if node["_maxheight"] > 0:
            markdown_string += "\n\n"
            html_string += "\n"
    else:
        raise ValueError(f"Unknown meta type: {node_type}")

    return {"html": html_string, "markdown": markdown_string, "text": text_string}


def as_dict(node):
    children_list = {}
    for child in node["children"]:
        for child_name, child_dict in as_dict(child).items():
            children_list[child_name] = child_dict
    return {node["name"]: children_list}


def plain_text(html):
    soup = bs(html or "", features="lxml")
    for sup in soup.find_all("sup"):
        sup.decompose()
    return soup.get_text(" ", strip=True)


def describe_node(node, rendered_html):
    text = plain_text(rendered_html)
    if not text:
        text = "Read the Book of Doctrine from the Church of God (Deist)."
    return text[:157].rsplit(" ", 1)[0] + "..." if len(text) > 160 else text


def page_title(node):
    if node["parent"] is None:
        return "Book of Doctrine | Church of God (Deist)"
    names = [a["name"] for a in get_ancestors(node)][1:]
    return " | ".join(names + ["Book of Doctrine"])


def seo_tags(node, rendered_html):
    title = html_lib.escape(page_title(node), quote=True)
    description = html_lib.escape(describe_node(node, rendered_html), quote=True)
    url = SITE_URL + gen_url(node)
    json_ld = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": page_title(node),
        "url": url,
        "isPartOf": {
            "@type": "Book",
            "name": "Book of Doctrine",
            "url": SITE_URL + "/",
        },
    }
    return "\n".join(
        [
            '<meta charset="utf-8" />',
            '<meta name="viewport" content="width=device-width, initial-scale=1" />',
            f'<meta name="description" content="{description}" />',
            '<meta name="robots" content="index, follow, max-image-preview:large" />',
            f'<link rel="canonical" href="{url}" />',
            f'<meta property="og:title" content="{title}" />',
            f'<meta property="og:description" content="{description}" />',
            f'<meta property="og:url" content="{url}" />',
            '<meta property="og:type" content="article" />',
            f'<script type="application/ld+json">{json.dumps(json_ld, separators=(",", ":"))}</script>',
        ]
    )


def canon_id(node, fallback_index):
    parts = [slugify(a["name"]).upper() for a in get_ancestors(node)]
    return ".".join(parts + [f"{fallback_index:04d}"])


def build_canon_records(root):
    records = []
    generated_urls = set(root.get("staticUrls", []))

    def containing_page_url(node):
        current = node
        while current is not None:
            url = gen_url(current)
            if url in generated_urls or current["parent"] is None:
                return url
            current = current["parent"]
        return "/"

    def visit(node):
        if node["meta"].get("ignore"):
            return
        rendered = to_markdown(node)
        text = plain_text(rendered["html"])
        if text and node["_maxheight"] == 0:
            ancestors = get_ancestors(node)
            records.append(
                {
                    "id": canon_id(node, len(records) + 1),
                    "work": root["name"],
                    "path": [ancestor["name"] for ancestor in ancestors],
                    "title": node["name"],
                    "text": text,
                    "url": containing_page_url(node),
                    "canonicalUrl": SITE_URL + containing_page_url(node),
                    "type": node["meta"].get("type", "default"),
                    "references": node["meta"].get("reference", []),
                }
            )
        for child in node["children"]:
            visit(child)

    visit(root)
    return {
        "site": SITE_URL,
        "work": root["name"],
        "generated": date.today().isoformat(),
        "records": records,
    }


def build_sitemap(root):
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    seen = set()
    urls = root.get("staticUrls", ["/"])
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        priority = "1.0" if url == "/" else "0.8" if url.count("/") <= 2 else "0.6"
        lines.extend(
            [
                "  <url>",
                f"    <loc>{html_lib.escape(SITE_URL + url)}</loc>",
                f"    <lastmod>{today}</lastmod>",
                "    <changefreq>weekly</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def export_static(node, index=0, value=1000.0, build_dir=None, template="SELECTED_NODE_TEXT"):
    if build_dir is None:
        build_dir = get_apex(node)["buildDir"]

    retdict = {
        "url": gen_url(node),
        "name": node["name"],
        "children": [],
        "indexedName": f"{index}\n\n{node['name']}",
        "meta": node["meta"],
    }

    if node["_maxheight"] <= 1:
        retdict["value"] = value
        if node["parent"] is not None:
            retdict["parent"] = node["parent"]["name"]
    else:
        sf_sum = sum("skipFlare" not in c["meta"] for c in node["children"])
        if sf_sum == 0:
            sf_sum = 1
        value = value / sf_sum
        child_index = 0
        for child in node["children"]:
            if "skipFlare" not in child["meta"]:
                retdict["children"].append(
                    export_static(child, index=child_index, value=value, build_dir=build_dir, template=template)
                )
                child_index += 1

    prefix = asset_prefix(node)
    node_render = to_markdown(node)
    retdict["text"] = node_render["html"]
    this_html = template.replace("SELECTED_NODE_TEXT", node_render["html"])
    this_html = this_html.replace("PAGE_TITLE", html_lib.escape(page_title(node), quote=True))
    this_html = this_html.replace("SEO_META", seo_tags(node, node_render["html"]))
    this_html = this_html.replace("ASSET_VERSION", ASSET_VERSION)
    this_html = this_html.replace("ASSET_PREFIX", prefix)
    this_html = this_html.replace("BACK_ARROW_LINK", gen_url(get_elder_sibling(node)))
    this_html = this_html.replace("FORWARD_ARROW_LINK", gen_url(get_younger_sibling(node)))
    if node["parent"] is not None:
        this_html = this_html.replace("UP_ARROW_LINK", gen_url(node["parent"]))
    else:
        this_html = this_html.replace("UP_ARROW_LINK", node["url"])

    base_dir = os.path.join(build_dir, *[slugify(a["name"]) for a in get_ancestors(node)[:-1]])
    os.makedirs(base_dir, exist_ok=True)
    write_text(Path(build_dir) / node["path"], this_html)
    static_urls = get_apex(node).setdefault("staticUrls", [])
    url = gen_url(node)
    if url not in static_urls:
        static_urls.append(url)

    return retdict


def ensure_clean_build():
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    shutil.copytree(SRC_DIR, BUILD_DIR)
    for generated_path in (
        BUILD_DIR / "book_of_doctrine",
        BUILD_DIR / "book_of_doctrine.html",
        BUILD_DIR / "julian.json",
        BUILD_DIR / "julian_flare.json",
        BUILD_DIR / "canon.json",
        BUILD_DIR / "sitemap.xml",
        BUILD_DIR / "ABSA.html",
        BUILD_DIR / "README.md",
    ):
        if generated_path.is_dir():
            shutil.rmtree(generated_path)
        elif generated_path.exists():
            generated_path.unlink()


def write_text(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    print(f"writing {path}")
    path.write_text(content, encoding="utf-8")


def write_landing_page():
    landing_html = (SRC_DIR / "landing.html").read_text(encoding="utf-8")
    landing_html = landing_html.replace("ASSET_VERSION", ASSET_VERSION)
    write_text(BUILD_DIR / "index.html", landing_html)


def copy_tree(src, dest):
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main():
    sys.path.insert(0, str(BOOK_DIR))
    context = {"nodeNumber": 0}

    root = build_from_directory(BOOK_DIR, parent=None, depth=1, context=context)
    root["buildDir"] = str(BUILD_DIR)
    root["graphsDir"] = GRAPHS_DIR_NAME
    root["displayVerseNo"] = True
    root["align"] = "left"
    root["textColor"] = "black"
    root["verseNo"] = 0
    root["referenceNo"] = 0
    root["skipGraphs"] = False
    root["staticUrls"] = ["/", "/book_of_doctrine/"]

    compute_height_no_lists(root)
    sort_children_by_priority(root)

    ensure_clean_build()

    template = (SRC_DIR / "index_template.html").read_text(encoding="utf-8")
    template = template.replace('<li><a href="javascript:void(0)" id="deismuButton" class="dropbtn">DeismU</a></li>', "")
    template = template.replace('<li><a href="javascript:void(0)" id="profileButton" class="dropbtn">Profile</a></li>', "")
    template = template.replace('<li><a href="javascript:void(0)" id="loginButton" class="dropbtn">Login</a></li>', "")
    flare = export_static(root, template=template, build_dir=str(BUILD_DIR))
    flare_json = json.dumps(flare, indent=2)

    write_text(BUILD_DIR / "julian_flare.json", flare_json)

    write_text(BUILD_DIR / "julian.json", json.dumps(as_dict(root), indent=2))
    write_text(BUILD_DIR / "canon.json", json.dumps(build_canon_records(root), indent=2))
    write_text(BUILD_DIR / "sitemap.xml", build_sitemap(root))
    write_landing_page()

    out = to_markdown(root)
    html_string = bs(out["html"], features="lxml").prettify()
    write_text(BUILD_DIR / "ABSA.html", html_string)
    write_text(BUILD_DIR / "README.md", out["markdown"])

    # Build output only; do not copy back into src.


if __name__ == "__main__":
    main()
