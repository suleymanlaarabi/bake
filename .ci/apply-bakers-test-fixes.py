from pathlib import Path

p = Path('bake-rust-port/src/env.rs')
s = p.read_text()
old = '''pub fn dependency_available(build_env: &BuildEnvironment, id: &str, static_lib: bool) -> bool {
    if source_for(build_env, id).is_some() || build_env.meta.join(id).join("project.json").exists() {
        return true;
    }
    library_candidates(build_env, id, static_lib)
        .into_iter()
        .any(|path| path.exists())
}
'''
new = '''pub fn dependency_available(build_env: &BuildEnvironment, id: &str, static_lib: bool) -> bool {
    if library_candidates(build_env, id, static_lib)
        .into_iter()
        .any(|path| path.exists())
    {
        return true;
    }

    let manifest = build_env.meta.join(id).join("project.json");
    if let Ok(config) = crate::config::ProjectConfig::load(&manifest) {
        return config.language() == "none";
    }
    false
}
'''
if old not in s:
    raise SystemExit('dependency_available pattern not found')
p.write_text(s.replace(old, new, 1))
