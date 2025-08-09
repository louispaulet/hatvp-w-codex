# HATVP with Codex

HATVP with Codex is an exploration of how OpenAI's Codex models can help analyse official French transparency reports. The goal is to automatically read declarations published by the *Haute Autorité pour la transparence de la vie publique* (HATVP) and produce structured summaries and insights.

## What is the HATVP?

The HATVP is an independent French authority that promotes transparency in public life by collecting and publishing declarations of interests and assets from elected officials and senior public servants. These disclosures help citizens understand potential conflicts of interest and foster trust in democratic institutions.

## Why transparency matters

Open access to information about public officials’ finances is a cornerstone of democratic accountability. By making disclosures easier to analyse, citizens, journalists and researchers can more effectively monitor how power is exercised and ensure that decisions are made in the public interest.

## About OpenAI Codex

OpenAI Codex is a model capable of understanding and generating code in many programming languages. In this project we investigate how Codex can be used to parse the XML declarations released by the HATVP and generate human‑readable reports or datasets that make the information more accessible.

## Repository structure

- **split_declarations/** – sample dataset of individual declaration files created from the official bulk XML release. Each file contains metadata such as the deposit date, UUID and attached PDF references.
- **script_to_split_declarations.py** – utility used to split the original massive `declarations.xml` file into separate XML documents, one per declaration.

This README is intentionally brief and will be expanded as the project evolves.

