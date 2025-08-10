# Wikipedia Summary Stats

## Coverage of current dataset
- Total people in base dataset (`avis/NER/people.csv`): 253
- People with valid summaries (`found_summaries_for_people.csv`): 136
- Coverage: 53.8%
- Missing: 117 (46.2%)

## Projection for 12k name lookups
Assuming match rate remains ~53.8% and each lookup takes about 1 second:
- Expected matched summaries: ~6,451
- Estimated lookup time: ~3.3 hours
- Average summary length: ~33 tokens (~25 words)
- Estimated total tokens for matched summaries: ~211k tokens

Token counts are estimated using an average of 1.33 tokens per word.
