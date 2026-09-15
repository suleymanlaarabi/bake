from pathlib import Path

def replace(path, old, new, count=1):
    p = Path(path)
    s = p.read_text()
    if old not in s:
        raise SystemExit(f"pattern not found in {path}: {old[:80]!r}")
    p.write_text(s.replace(old, new, count))

# env.rs: allow paths and strings in env vars + clippy collapses.
replace(
    'bake-rust-port/src/env.rs',
    '    env, fs,\n    path::{Path, PathBuf},',
    '    env, fs,\n    ffi::OsStr,\n    path::{Path, PathBuf},',
)
replace(
    'bake-rust-port/src/env.rs',
    'fn set_var(name: &str, value: &Path) {\n    unsafe { env::set_var(name, value) };\n}',
    'fn set_var(name: &str, value: impl AsRef<OsStr>) {\n    unsafe { env::set_var(name, value) };\n}',
)
replace(
    'bake-rust-port/src/env.rs',
    '    if let Some(rest) = value.strip_prefix("~/") {\n        if let Some(base) = env::var_os("HOME").or_else(|| env::var_os("USERPROFILE")) {\n            return PathBuf::from(base).join(rest);\n        }\n    }',
    '    if let Some(rest) = value.strip_prefix("~/")\n        && let Some(base) = env::var_os("HOME").or_else(|| env::var_os("USERPROFILE"))\n    {\n        return PathBuf::from(base).join(rest);\n    }',
)
replace(
    'bake-rust-port/src/env.rs',
    '    if source_file.exists() {\n        if let Ok(text) = fs::read_to_string(source_file) {\n            let path = PathBuf::from(text.trim());\n            if path.join("project.json").exists() {\n                return Some(path);\n            }\n        }\n    }',
    '    if source_file.exists()\n        && let Ok(text) = fs::read_to_string(source_file)\n    {\n        let path = PathBuf::from(text.trim());\n        if path.join("project.json").exists() {\n            return Some(path);\n        }\n    }',
)
replace(
    'bake-rust-port/src/env.rs',
    '            if entry.path().is_dir() {\n                if let Some(name) = entry.file_name().to_str() {\n                    out.insert(name.to_owned());\n                }\n            }',
    '            if entry.path().is_dir()\n                && let Some(name) = entry.file_name().to_str()\n            {\n                out.insert(name.to_owned());\n            }',
)

# config.rs: use conditional parser and satisfy clippy without suppressions.
replace(
    'bake-rust-port/src/config.rs',
    '        let mut raw = parse_json_with_comments(&text)\n            .with_context(|| format!("parsing {}", path.display()))?;\n        raw = apply_conditionals(raw, ctx)?;',
    '        let mut raw = parse_value_with_context(&text, ctx)\n            .with_context(|| format!("parsing {}", path.display()))?;',
)
replace(
    'bake-rust-port/src/config.rs',
    '        if !value_object.contains_key(canonical) {\n            if let Some(value) = value_object.remove(alias) {\n                value_object.insert(canonical.into(), value);\n            }\n        }',
    '        if !value_object.contains_key(canonical)\n            && let Some(value) = value_object.remove(alias)\n        {\n            value_object.insert(canonical.into(), value);\n        }',
)
replace(
    'bake-rust-port/src/config.rs',
    '                if let Some(id) = item.as_str() {\n                    if id.contains(\'/\') {\n                        *item = Value::String(id.replace(\'/\', "."));\n                    }\n                }',
    '                if let Some(id) = item.as_str()\n                    && id.contains(\'/\')\n                {\n                    *item = Value::String(id.replace(\'/\', "."));\n                }',
)
replace(
    'bake-rust-port/src/config.rs',
    '    if let Some(Value::String(language)) = value_object.get_mut("language") {\n        if language == "c++" {\n            *language = "cpp".into();\n        }\n    }',
    '    if let Some(Value::String(language)) = value_object.get_mut("language")\n        && language == "c++"\n    {\n        *language = "cpp".into();\n    }',
)
replace(
    'bake-rust-port/src/config.rs',
    '    if !value_object.contains_key("amalgamate") {\n        if let Some(amalgamate) = top_level_amalgamate {\n            value_object.insert("amalgamate".into(), amalgamate);\n        }\n    }',
    '    if !value_object.contains_key("amalgamate")\n        && let Some(amalgamate) = top_level_amalgamate\n    {\n        value_object.insert("amalgamate".into(), amalgamate);\n    }',
)

# project.rs: dead helper removal + clippy collapse.
replace(
    'bake-rust-port/src/project.rs',
    '            if let Some(candidate) = by_id.get(dependency) {\n                if !seen.contains(dependency) {\n                    queue.push_back(candidate.clone());\n                }\n            }',
    '            if let Some(candidate) = by_id.get(dependency)\n                && !seen.contains(dependency)\n            {\n                queue.push_back(candidate.clone());\n            }',
)
p = Path('bake-rust-port/src/project.rs')
s = p.read_text()
start = s.find('\npub fn project_store(home: &Path) -> PathBuf {')
end_marker = '\n    discover_recursive(&store)\n}\n'
if start == -1:
    raise SystemExit('project_store block not found')
end = s.find(end_marker, start)
if end == -1:
    raise SystemExit('discover_store end not found')
end += len(end_marker)
p.write_text(s[:start] + '\n' + s[end:])

replace(
    'bake-rust-port/src/build.rs',
    '        if cache.exists() {\n            if let Some(root) = cache.parent() {\n                fs::remove_dir_all(root)?;\n            }\n        }',
    '        if cache.exists()\n            && let Some(root) = cache.parent()\n        {\n            fs::remove_dir_all(root)?;\n        }',
)
replace(
    'bake-rust-port/src/main.rs',
    '                if recursive {\n                    if let Some(url) = repository_for(&projects, dependency) {\n                        let cloned = clone_dependency(dependency, &url, opts)?;\n                        for project in cloned {\n                            if !ids.contains(&project.id)\n                                && !added.iter().any(|current: &Project| current.id == project.id)\n                            {\n                                added.push(project);\n                            }\n                        }\n                        continue;\n                    }\n                }',
    '                if recursive\n                    && let Some(url) = repository_for(&projects, dependency)\n                {\n                    let cloned = clone_dependency(dependency, &url, opts)?;\n                    for project in cloned {\n                        if !ids.contains(&project.id)\n                            && !added.iter().any(|current: &Project| current.id == project.id)\n                        {\n                            added.push(project);\n                        }\n                    }\n                    continue;\n                }',
)
