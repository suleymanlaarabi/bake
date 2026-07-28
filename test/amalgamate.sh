#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
bake_bin=${BAKE:-bake}
cc_bin=${CC:-cc}
out_dir=$(mktemp -d /tmp/bake-amalgamate-test.XXXXXX)

cleanup() {
    rm -rf "$out_dir"
}
trap cleanup EXIT

conditional="$repo_root/examples/c/pkg_amalgamate_conditional"
generated="$conditional/generated"
main="$conditional/standalone/main.c"

build_case() {
    name=$1
    shift
    "$cc_bin" -std=c99 "$@" \
        "$generated/amalgamate_conditional.c" "$main" \
        -I"$generated" -o "$out_dir/$name"
    "$out_dir/$name"
}

# No condition, either condition, and both conditions must all be valid
# standalone translation units.
build_case none
build_case public -DAMALGAMATE_WITH_PUBLIC
build_case private -DAMALGAMATE_WITH_PRIVATE
build_case both -DAMALGAMATE_WITH_PUBLIC -DAMALGAMATE_WITH_PRIVATE

# Disabled packages must not contribute symbols.
! nm "$out_dir/none" | grep -Eq \
    'amalgamate_(leaf|dependency|private)_value'
! nm "$out_dir/public" | grep -q 'amalgamate_private_value'
! nm "$out_dir/private" | grep -q 'amalgamate_dependency_value'

# The shared transitive leaf is merged under the OR condition and emitted once.
test "$(grep -c '^int amalgamate_leaf_value' \
    "$generated/amalgamate_conditional.c")" -eq 1
grep -q \
    '#if (AMALGAMATE_WITH_PRIVATE) || (AMALGAMATE_WITH_PUBLIC)' \
    "$generated/amalgamate_conditional.c"

# Dependencies precede dependents, and the second output has its own closure.
leaf_line=$(grep -n '^int amalgamate_leaf_value' \
    "$generated/amalgamate_conditional.c" | cut -d: -f1)
dependency_line=$(grep -n '^int amalgamate_dependency_value' \
    "$generated/amalgamate_conditional.c" | cut -d: -f1)
project_line=$(grep -n '^int amalgamate_conditional_value' \
    "$generated/amalgamate_conditional.c" | cut -d: -f1)
test "$leaf_line" -lt "$dependency_line"
test "$dependency_line" -lt "$project_line"
! grep -q '^int amalgamate_private_value' \
    "$conditional/generated-public/amalgamate_conditional.c"

# Generation is reproducible.
cp "$generated/amalgamate_conditional.c" "$out_dir/before.c"
cp "$generated/amalgamate_conditional.h" "$out_dir/before.h"
"$bake_bin" rebuild "$conditional" >/dev/null
cmp "$out_dir/before.c" "$generated/amalgamate_conditional.c"
cmp "$out_dir/before.h" "$generated/amalgamate_conditional.h"

# Invalid dependency descriptions fail during project parsing.
for fixture in "$repo_root"/test/amalgamate_invalid/*; do
    "$bake_bin" rebuild "$fixture" >"$out_dir/invalid.log" 2>&1 || true
    grep -q 'failed to parse' "$out_dir/invalid.log"
done
