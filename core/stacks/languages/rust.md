---
id: rust
title: Rust
kind: language
applies_to: ["**/*.rs"]
related: []
volatility: volatile
reviewed: 2026-10-09
sources: ["https://doc.rust-lang.org/book/", "https://doc.rust-lang.org/cargo/", "https://doc.rust-lang.org/edition-guide/", "https://rust-lang.github.io/api-guidelines/", "https://blog.rust-lang.org/"]
---

# Rust

## Detect
- `Cargo.toml`: `[workspace]` members and `[workspace.dependencies]`, per-crate `edition`, `rust-version` (MSRV), `[features]`, `[lints]`.
- Toolchain: `rust-toolchain.toml` (channel, components, targets); nightly-only features require that channel.
- Config: `.cargo/config.toml` (targets, aliases, rustflags), `clippy.toml`, `rustfmt.toml`, `deny.toml`, `build.rs`.
- Crate kind: library (`src/lib.rs`) or binary (`src/main.rs`); crate attributes such as `#![no_std]` and `#![forbid(unsafe_code)]`.
- Async runtime and error crates among dependencies (for example `tokio`, `thiserror`, `anyhow`).

## Conventions
- Return `Result` and propagate with `?`. Libraries expose typed error enums (the `thiserror` pattern); applications add context with an `anyhow`-style error type. Follow the crates already in use.
- No `unwrap()` or `expect()` in library or request paths; use `expect("reason")` only for invariants proven at that point. Tests may unwrap.
- Borrow before cloning: accept `&str`, `&[T]`, `impl AsRef<_>`; return owned types.
- Use `Arc<Mutex<_>>` or `Rc<RefCell<_>>` only when shared mutation is required; otherwise transfer ownership or pass messages.
- `unsafe` only when no safe alternative exists: smallest possible block, a `// SAFETY:` comment stating the invariants upheld, wrapped in a safe API, and never where crate lints forbid it.
- Keep Cargo features additive: enabling a feature never removes API or changes existing behavior.
- In async code, never block the executor (use async I/O or `spawn_blocking`) and never hold a `std::sync::Mutex` guard across `.await`.
- Derive `Debug` (and `Clone`, `PartialEq`, `Eq`, `Hash` where meaningful) on public types; document public items with `///`.
- Use no std API newer than `rust-version`.

## Verify
- Format: `commands.format`, or `cargo fmt --all -- --check`.
- Lint: `commands.lint`, or `cargo clippy --workspace --all-targets --all-features -- -D warnings`.
- Tests: `commands.test`, or `cargo test --workspace`; narrow with `cargo test -p <crate> <name_filter>`. When the project uses `cargo nextest run`, also run `cargo test --doc`, because nextest skips doctests.
- Crates with optional features: also `cargo check --no-default-features`.

## Pitfalls
- Cloning to silence the borrow checker hides an ownership problem; restructure ownership or lifetimes first.
- Integer overflow panics in debug builds but wraps in release; use `checked_*`, `saturating_*`, or `wrapping_*` explicitly.
- `as` casts truncate silently; use `TryFrom`/`try_into()` for fallible conversions.
- `cargo update` without `-p <crate>` bumps unrelated dependencies in `Cargo.lock`.
- Holding a `RefCell` borrow or lock guard while calling code that borrows again panics or deadlocks; drop it first.
- Non-additive features break downstream crates, because Cargo unifies features across the dependency graph.

## Version Notes
- Edition 2024 is stable since Rust 1.85. In it, `std::env::set_var`/`remove_var` are `unsafe`, `extern` blocks need `unsafe extern`, `#[no_mangle]` becomes `#[unsafe(no_mangle)]`, and Cargo defaults to the MSRV-aware resolver `"3"` (as of 2026-10, per doc.rust-lang.org edition-guide).
- Migrate editions with `cargo fix --edition` as a separate change, never mixed into feature work.
- Async closures (`async || {}`) are stable since 1.85 (as of 2026-10, per blog.rust-lang.org).
- Stable releases ship every six weeks; check `rust-version` and `rust-toolchain.toml` before using a recently stabilized API (as of 2026-10, per blog.rust-lang.org).
