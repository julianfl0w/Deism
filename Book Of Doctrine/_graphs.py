from pathlib import Path
import ast


_BASE_DIR = Path(__file__).resolve().parent


def _load_data(path: Path):
    source = path.read_text(encoding="utf-8")
    module = ast.parse(source, filename=str(path))
    globals_dict = {"__file__": str(path)}

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

    raise ValueError(f"No data expression or DATA/GRAPH/CONTENT in {path}")


def graph(relative_path: str):
    return _load_data(_BASE_DIR / relative_path)
