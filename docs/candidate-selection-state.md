# Candidate selection status

A Phase 2 candidate's decision is held in two 0/1 columns, `ind_session` and `ind_waitlist`. Left as two flags, every panel that reads them re-derives the status on its own, and a row with both set is Selected in one panel and counted twice in another. The status is therefore declared as one closed type, `CandidateStatus`, with one derive function, `candidate_status`, in `content/metadata/selection_status.py`. The machine is registered as `candidate_status` in `.fleet.toml` (`[[state_machines]]`).

## States

| State | `ind_session` | `ind_waitlist` | Meaning |
|---|---|---|---|
| Selected | 1 | 0 | Chosen for the session |
| Waitlist | 0 | 1 | Held in reserve |
| Pending | 0 | 0 | No decision yet |
| Conflict | 1 | 1 | Both set: an impossible decision, shown as its own state and counted once |
| Unknown | blank or not 0/1 | any | A flag could not be read; never folded into Pending |

A column the row does not have reads as 0. The loaders turn blank cells into 0 before any tab sees the frame, so Unknown only appears for a value outside 0/1.

## Transitions

The Phase 2 editor sets the two flags. They are exclusive: on save, `exclusive_flags` keeps the flag that was ticked last and clears the other, and keeps Selected when both were ticked at once or an old conflict is saved untouched. The bulk buttons in Selection Management write one flag at a time on rows in a single state, so they cannot create a Conflict; "Reset All to Pending" clears both.

## Who reads it

| Reader | Calls |
|---|---|
| Explore tab: metrics and hierarchy breakdown | `status_counts`, `status_table` |
| Selection Management: summary, candidate list, team balance, quick actions, report | `status_counts`, `status_column`, `status_table` |
| Phase 2 Entry: team balance and decision table | `status_counts`, `candidate_status` |

A new reader calls these and never compares `ind_session` or `ind_waitlist` to decide a status. Pending on the Explore tab counts confirmed candidates only, the same rows as Selection Management.

## Test

`content/metadata/test_selection_status.py` has one row per flag combination (0, 1, blank, out of range), the count invariants, and the tests that carry the `state-machine-proof: candidate_status` marker: a saved row is never Conflict and a Conflict row is never read as Selected or Waitlist. Run it from `content/metadata/` with `python -m unittest test_selection_status`.
