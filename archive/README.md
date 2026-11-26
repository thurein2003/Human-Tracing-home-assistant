# Recovery and revision index

The [recovery manifest](recovery-manifest.csv) maps original workspace-relative paths to archive destinations, with original sizes, SHA-256 hashes, staged hashes, file classes, revision groups and timestamps. The full original-path inventory and primary ZIP member index are stored in the local review workspace outside Git.

The earlier timestamped CAD tree, integrated candidate and expanded Final Engineering tree are preserved under [engineering](engineering). Start with [mechanical design](../docs/mechanical.md) for the corrected models. Selected named artifacts were promoted into hardware and identical byte streams are represented once. Historical relative links can point to promoted paths, held media or deduplicated rows. Resolve those paths using the manifest. Historical reports and tools reflect their original date and scope.

When a text release copy requires removal of an absolute workstation path, the original and staged hashes differ. The earlier archives retain exact original source bytes locally. The primary delivery ZIP matched its supplied SHA-256, opened successfully and was copied with its checksum into the local delivery workspace. Nested workstation paths and unreviewed images put the exact ZIP outside the publication commit. Source archives, ambiguous engineering binaries and unreviewed visuals remain at their original locations. Review any original third-party attribution or sharing requirements before further redistribution. No new project license was assigned.

No live Raspberry Pi source files were recovered. The archived Python and macro files are mechanical engineering tools and do not contain the operational controller.


The [duplicate index](exact-duplicates.csv) records 2,111 distinct source hashes across 2,851 original files. It lists 291 byte streams with multiple original paths.
