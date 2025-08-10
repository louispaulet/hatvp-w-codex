# count_organization_mentions.py

**Inputs:** name lists from `avis/NER/organizations.csv` and `avis/NER/people.csv`,
 declaration XML files in `split_declarations/`

**Outputs:** `organization_mentions.csv`, `people_mentions.csv`

Searches each declaration for occurrences of specified organization and person names.
