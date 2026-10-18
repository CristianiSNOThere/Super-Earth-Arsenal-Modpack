# Incremental regression policy

## Rule

**Test the change and its shared consumers. Do not repeat the entire baseline
combination matrix or require testing every existing mod for a routine
addition.** Use the accepted catalog, resource hashes and startup contract as
the regression baseline. This rule reduces repeated tests; it does not waive
unknown-value guards, partial-write rollback, actual transaction checks or
playtester acceptance for new behavior.

### Every change

For custom numeric damage/projectile IDs, also check active native lookup
ownership. A serialized row can retain the intended values while its registry
entry points to another runtime's copy. Static Addon resource compatibility does
not detect that collision. Include redirected-registry cases for the changed
profiles, refuse unknown owners and preserve foreign rows/pointers. The captured
Variable failure at damage IDs542-544 is a reusable regression case; it does not
require repeating old weapon combinations or a live memory capture for every mod.

1. Name the changed modules/resources/options and pin the game, loader and
   Arsenal versions used. Verify that unrelated payload hashes remain exact.
2. Check the complete catalog for differing shared-resource collisions and
   missing module dependencies. Compile changed Lua, inspect the actual ZIP,
   preserve stable identities and keep Lua archives separate from animations.
   This full inventory check is inexpensive; it does not require enumerating
   every selection or launching every weapon.
   Compare CPU, GPU and STREAM payloads, not CPU bytes alone. FileData records
   must keep each resource type contiguous with exact type counts and row
   indices. The native loader allocates NumTypes*40 bytes but starts another
   group on each uncached type transition; interleaved records can overflow it.
   Punisher's Rev8/Rev9 saved-native-code fixture is the regression case. A boot
   package required by a mod must have an explicit owner/dependency closure in
   a separate non-Lua archive; never relax the pure-Lua check to accommodate it.
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
- For source changes required before native equipment creation, exercise a
  saved equipped loadout against realistically delayed companions. A whole-pack
  readiness wait must not postpone those source changes past equipment restore.
  Preserve exact source/ownership/absence/native-transaction guards. If peer
  completion follows installation, retain bounded named waits and validate only
  exact supported peer variants before observation; preserve unknown/foreign edits.
  Punisher Rev1's pre-ship failure and Rev3's 7s/30s scheduling fixtures cover
  this case. Immediate-ready startup adapters alone do not cover the deadline.
- Run one combined full-pack configuration after the addition, using the
  existing startup-control/dependency fixtures. A new unrelated private key
  does not require retesting every pair or triple of old mods.
- Obtain a fresh playtester startup/gameplay check of the new behavior and a
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
fresh playtester launches. Keep deployment, settings and gameplay under player control.
Publishing and retirement of the individual repository remain separately
authorized actions; retain release history and immutable candidates.
