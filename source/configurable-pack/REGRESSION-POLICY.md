# Incremental checks for future mod changes

Requested by the user on 2026-10-15 after the selectable-pack migration. The
initial broad offline matrix is retained as evidence. A fresh four-mod Rev2
launch at 16:02:19 local applied APW-1, P-34, CQC-20 and Railgun: four profiles,
nine values, 41 modules loaded, zero loader failures, 12 exact deployed file
matches. This is startup evidence for that selection; gameplay acceptance and
the remaining v2 release checks are separate.

Full22Rev3startup at16:16:44 local is also confirmed:61loaded/0failed,
all22expected final states and75exact deployed files; Flagdefault300/150applied.
Both startup selections are accepted baseline evidence; v2.0.0 was subsequently
published at the user request. Do not infer universal gameplay.

## v2.1.0 accepted extension

AdjudicatorHeavy adds one private option/resource pair; existing22gameplay
archives and29Flagpresets are exact. Rev2full23startup18:59:51Europe/Madrid
passes62loaded/0failed,all23finalstates,78deployedfiles. Useraccepts480RPM and
requests publication. Incrementalchecks cover30actualBR-14transactions,
targetedstartup/faultcases,fullresourceclosure,6Arsenaldeployments andoldoption
migration. The oldmigrationmatrix was reused rather than repeated.

## Rule

**Test the change and its shared consumers. Do not repeat the entire baseline
combination matrix or ask the user to test every existing mod for a routine
addition.** Use the accepted catalog, resource hashes and startup contract as
the regression baseline. This rule reduces repeated tests; it does not waive
unknown-value guards, partial-write rollback, actual transaction checks or
user gameplay acceptance for new behavior.

### Every change

1. Name the changed modules/resources/options and pin the game, loader and
   Arsenal versions used. Verify that unrelated payload hashes remain exact.
2. Check the complete catalog for differing shared-resource collisions and
   missing module dependencies. Compile changed Lua, inspect the actual ZIP,
   preserve stable identities and keep Lua archives separate from animations.
   This full inventory check is inexpensive; it does not require enumerating
   every selection or launching every weapon.
3. Exercise actual changed transactions in isolated memory: stock success,
   unknown data refusal, ownership checks, partial writes/readback, rollback and
   preservation of foreign changes. Reuse unchanged fixture results when their
   code, data and relevant dependencies have identical hashes.

### New weapon or changed gameplay module

- Test it alone and with each mod that shares its tables/status/animation,
  modifies a recognized peer value, or participates in its readiness path.
- Test both startup orders for those interactions, absent/late/failed peers,
  and every supported peer state accepted by any changed validator. Include
  mixed peer states only where the validator actually combines their changes.
- Run one combined full-pack configuration after the addition, using the
  existing startup-control/dependency fixtures. A new unrelated private key
  does not require retesting every pair or triple of old mods.
- Ask for a fresh user startup/gameplay check of the new behavior and a
  representative combined startup. Combine those checks in one launch when
  the scenario covers both gates. Additional launches require a concrete
  affected path or observed failure; no manual checklist of all weapons.

### Manifest, options or packaging only

- Run real Arsenal import/deployment/purge in isolated folders for all-off,
  changed option alone, relevant peer set, a known small subset and full pack.
- Exercise every new radio choice and default, parent disabled, migration,
  profile-versus-library selection, archive numbering and loader discovery
  order where it matters. Preserve all unrelated gameplay resource bytes.
- Reuse the broad startup/transaction baseline if its code and dependencies
  are exact. Do not rerun thousands of startup simulations or all prior
  transaction suites just because an option label/folder/preset changed.

The Flag single-dropdown revision follows this route: 64 focused Arsenal
deployments, all 29 presets with actual Flag writes and SAI/Gas guard checks,
two actual discovery-order fixtures, and exact old gameplay-resource hashes.

### When to broaden testing

Broaden only the affected scope if a shared runtime, loader/discovery contract,
common validator, serialized layout, game fingerprint or Arsenal option schema
changes, or if a failure invalidates the prior baseline. State the concrete
reason and run the suites that depend on it. Use an explicit baseline migration
for changes that affect the whole set; do not silently bypass guards or assume
the old baseline remains valid. Exhaustive selection enumeration is optional
when it resolves a real inventory/dependency risk, not a mandatory ritual.

### Evidence and release gates

Keep offline checks, actual loader startup, independent loaded-resource checks,
gameplay and host/client evidence distinct. A fixture adapter's Applied result
is not a live transaction. One working subset does not prove every game
combination. Save final module states and exact selected deployed bytes for
fresh user launches. Keep deployment, settings and gameplay with the user.
Publishing and retirement of the individual repository remain separately
authorized actions; retain release history and immutable candidates.
