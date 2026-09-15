from pathlib import Path


def replace(path, old, new):
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"pattern not found in {path}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1))


replace(
    'bake-rust-port/src/main.rs',
    "let normalized_id = id.replace('.', \"_\");",
    "let normalized_id = id.replace(['.', '/', '-'], \"_\");",
)
replace(
    'bake-rust-port/src/main.rs',
    "id.replace('.', \"-\")",
    "id.replace(['.', '/', '_'], \"-\")",
)
replace(
    'bake-rust-port/tests/integration.rs',
    'fs::write(lib.join("include/demo_lib.h"), "int answer(void);\\n").unwrap();',
    'fs::write(\n        lib.join("include/demo_lib.h"),\n        "#include \\\"demo-lib/bake_config.h\\\"\\nDEMO_LIB_API int answer(void);\\n",\n    )\n    .unwrap();',
)
replace(
    'bake-rust-port/tests/integration.rs',
    '"#include <demo_lib.h>\\n#ifdef _WIN32\\n__declspec(dllexport)\\n#endif\\nint answer(void){return 42;}\\n",',
    '"#include <demo_lib.h>\\nDEMO_LIB_API int answer(void){return 42;}\\n",',
)
