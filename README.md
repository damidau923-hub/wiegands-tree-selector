# Acme Nursery Tree Sales Assistant — POC v21

## Fix in v21: Flowering is now a hard requirement

When the salesperson chooses:

**Flowering tree? = Yes**

the search pool is restricted to trees marked as flowering **before** Full Match / Partial Match logic is applied.

Therefore:
- non-flowering trees cannot appear as Partial Matches
- broad-choice genera are built only from flowering candidates
- Quick Comparison and detailed cards also contain only flowering candidates

Likewise, choosing **No** restricts the search pool to non-flowering trees.

The rest of the matching logic is unchanged.
