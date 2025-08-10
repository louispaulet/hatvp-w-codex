# Dataset Documentation

## mandates_features.csv

**Description:** Detailed features for each political mandate, including identity, mandate type, documents and publication metadata.

**Columns:**

- **civilite** (object)
- **prenom** (object)
- **nom** (object)
- **classement** (object)
- **type_mandat** (object)
- **qualite** (object)
- **type_document** (object)
- **departement** (object)
- **date_publication** (object)
- **date_depot** (object)
- **nom_fichier** (object)
- **url_dossier** (object)
- **open_data** (object)
- **statut_publication** (object)
- **id_origine** (object)
- **url_photo** (object)
- **delay_days** (float64)
- **mandate_type** (object)

**Sample (first 5 rows):**

```csv
civilite,prenom,nom,classement,type_mandat,qualite,type_document,departement,date_publication,date_depot,nom_fichier,url_dossier,open_data,statut_publication,id_origine,url_photo,delay_days,mandate_type
Mme,Abbassia,HAKEM,hakemaaaabbassia4615,commune,Adjointe au maire de Nantes,di,44,2021-09-27,2020-09-01,hakem-abbassia-di16146-commune-nantes.pdf,/pages_nominatives/hakem-abbassia,hakem-abbassia-di16146-commune-nantes.xml,Livrée,,,391.0,commune
Mme,Abbassia,HAKEM,hakemaaaabbassia4615,commune,Adjointe au maire de Nantes,dim,44,2021-09-28,2021-08-02,hakem-abbassia-dim16147-commune-nantes.pdf,/pages_nominatives/hakem-abbassia,hakem-abbassia-dim16147-commune-nantes.xml,Livrée,,,57.0,commune
M.,Abdel Kader,CHEKHEMANI,chekhemaniaaaabdelkader1679,commune,Adjoint au maire de Rouen,di,76,2021-10-11,2020-10-14,chekhemani-abdel-kader-di16326-commune-rouen.pdf,/pages_nominatives/chekhemani-abdel-kader,chekhemani-abdel-kader-di16326-commune-rouen.xml,Livrée,,,362.0,commune
M.,Abdel Kader,CHEKHEMANI,chekhemaniaaaabdelkader1679,commune,Adjoint au maire de Rouen,dim,76,2021-10-12,2021-07-14,chekhemani-abdel-kader-dim16327-commune-rouen.pdf,/pages_nominatives/chekhemani-abdel-kader,chekhemani-abdel-kader-dim16327-commune-rouen.xml,Livrée,,,90.0,commune
M.,Abdelaziz,HAMIDA,HAMIDA Abdelaziz18939,commune,Maire de Goussainville,di,95,2021-08-10,2020-10-03,hamida-abdelaziz-di15206-commune-goussainville.pdf,/pages_nominatives/hamida-abdelaziz-18939,hamida-abdelaziz-di15206-commune-goussainville.xml,Livrée,,,311.0,commune
```

## pii/personal_info.csv

**Description:** Raw personal information extracted from declarations.

**Columns:**

- **file** (object)
- **dateDepot** (object)
- **uuid** (object)
- **civilite** (object)
- **nom** (object)
- **prenom** (object)
- **email** (object)
- **dateNaissance** (object)

**Sample (first 5 rows):**

```csv
file,dateDepot,uuid,civilite,nom,prenom,email,dateNaissance
000765d9-da68-48c6-a95d-f34a12cacb5f-20171221.xml,08/02/2021 19:58:13,000765d9-da68-48c6-a95d-f34a12cacb5f,M.,DELAPORTE,Olivier,[Données non publiées],29/07/1951
000b18d0-40c0-4edf-8bf5-e76841fe46df-20171221.xml,18/07/2023 09:47:16,000b18d0-40c0-4edf-8bf5-e76841fe46df,M.,Chaize,Patrick,[Données non publiées],22/03/1963
000e2a7c-5fae-4a8d-a1a4-8d04821effc7-20171221.xml,13/01/2025 12:00:37,000e2a7c-5fae-4a8d-a1a4-8d04821effc7,Mme,Meunier,Frederique,[Données non publiées],08/12/1960
000e41c4-3ae3-46b7-be32-1aa8b74c778b-20171221.xml,24/03/2025 23:24:20,000e41c4-3ae3-46b7-be32-1aa8b74c778b,M.,Gassilloud,Thomas,[Données non publiées],21/05/1981
00138e83-44ec-4da1-89f3-37d2309a62a2-20171221.xml,17/08/2020 19:27:35,00138e83-44ec-4da1-89f3-37d2309a62a2,Mme,SCHMITT,SYLVIE,[Données non publiées],04/04/1964
```

## pii/personal_info_enriched.csv

**Description:** Personal information with derived age and age bands.

**Columns:**

- **file** (object)
- **dateDepot** (object)
- **uuid** (object)
- **civilite** (object)
- **nom** (object)
- **prenom** (object)
- **email** (object)
- **dateNaissance** (object)
- **age** (float64)
- **age_band** (object)

**Sample (first 5 rows):**

```csv
file,dateDepot,uuid,civilite,nom,prenom,email,dateNaissance,age,age_band
000765d9-da68-48c6-a95d-f34a12cacb5f-20171221.xml,08/02/2021 19:58:13,000765d9-da68-48c6-a95d-f34a12cacb5f,M.,DELAPORTE,Olivier,[Données non publiées],29/07/1951,69.0,60-69
000b18d0-40c0-4edf-8bf5-e76841fe46df-20171221.xml,18/07/2023 09:47:16,000b18d0-40c0-4edf-8bf5-e76841fe46df,M.,Chaize,Patrick,[Données non publiées],22/03/1963,60.0,60-69
000e2a7c-5fae-4a8d-a1a4-8d04821effc7-20171221.xml,13/01/2025 12:00:37,000e2a7c-5fae-4a8d-a1a4-8d04821effc7,Mme,Meunier,Frederique,[Données non publiées],08/12/1960,64.0,60-69
000e41c4-3ae3-46b7-be32-1aa8b74c778b-20171221.xml,24/03/2025 23:24:20,000e41c4-3ae3-46b7-be32-1aa8b74c778b,M.,Gassilloud,Thomas,[Données non publiées],21/05/1981,43.0,40-49
00138e83-44ec-4da1-89f3-37d2309a62a2-20171221.xml,17/08/2020 19:27:35,00138e83-44ec-4da1-89f3-37d2309a62a2,Mme,SCHMITT,SYLVIE,[Données non publiées],04/04/1964,56.0,50-59
```

## pii/top_male_jobs.csv

**Description:** Most common occupations among male declarants and their pay grade.

**Columns:**

- **occupation** (object)
- **male** (int64)
- **female** (int64)
- **pay_grade** (object)

**Sample (first 5 rows):**

```csv
occupation,male,female,pay_grade
gerant,39,5,unknown
enseignant,37,3,unknown
ingenieur,24,8,high
commercial,18,0,unknown
agriculteur,17,0,unknown
```

## pii/spouse_activities.csv

**Description:** Professional activities of declarants' spouses.

**Columns:**

- **uuid** (object)
- **nomConjoint** (object)
- **employeurConjoint** (object)
- **activiteProf** (object)
- **commentaire** (object)

**Sample (first 5 rows):**

```csv
uuid,nomConjoint,employeurConjoint,activiteProf,commentaire
000b18d0-40c0-4edf-8bf5-e76841fe46df,[Données non publiées],SARL Peyrard,Commerce de vetements pour hommes,
000e2a7c-5fae-4a8d-a1a4-8d04821effc7,[Données non publiées],Societe Evidensia,vétérinaire,[Données non publiées]
000e41c4-3ae3-46b7-be32-1aa8b74c778b,[Données non publiées],SLEA,Travailleur social,
00138e83-44ec-4da1-89f3-37d2309a62a2,[Données non publiées],dekra,[Données non publiées],
0014115c-cbae-4bdd-98d1-39c8e6062095,[Données non publiées],SAS SLTS,[Données non publiées],[Données non publiées]
```

## pii/top_female_jobs.csv

**Description:** Most common occupations among female declarants and their pay grade.

**Columns:**

- **occupation** (object)
- **male** (int64)
- **female** (int64)
- **pay_grade** (object)

**Sample (first 5 rows):**

```csv
occupation,male,female,pay_grade
professeur des ecoles,7,126,high
enseignante,0,63,unknown
secretaire,0,47,low
infirmiere,0,46,low
journaliste,6,45,unknown
```

## pii/pay_grade_summary.csv

**Description:** Count of pay grades by gender.

**Columns:**

- **Unnamed: 0** (object)
- **high** (int64)
- **low** (int64)
- **unknown** (int64)

**Sample (first 5 rows):**

```csv
Unnamed: 0,high,low,unknown
male,9,1,10
female,5,5,10
```

## pii/personal_info_with_gender.csv

**Description:** Personal information dataset annotated with gender prediction.

**Columns:**

- **file** (object)
- **dateDepot** (object)
- **uuid** (object)
- **civilite** (object)
- **nom** (object)
- **prenom** (object)
- **email** (object)
- **dateNaissance** (object)
- **first_name** (object)
- **gender_guess** (object)
- **gender** (object)

**Sample (first 5 rows):**

```csv
file,dateDepot,uuid,civilite,nom,prenom,email,dateNaissance,first_name,gender_guess,gender
000765d9-da68-48c6-a95d-f34a12cacb5f-20171221.xml,08/02/2021 19:58:13,000765d9-da68-48c6-a95d-f34a12cacb5f,M.,DELAPORTE,Olivier,[Données non publiées],29/07/1951,Olivier,male,male
000b18d0-40c0-4edf-8bf5-e76841fe46df-20171221.xml,18/07/2023 09:47:16,000b18d0-40c0-4edf-8bf5-e76841fe46df,M.,Chaize,Patrick,[Données non publiées],22/03/1963,Patrick,male,male
000e2a7c-5fae-4a8d-a1a4-8d04821effc7-20171221.xml,13/01/2025 12:00:37,000e2a7c-5fae-4a8d-a1a4-8d04821effc7,Mme,Meunier,Frederique,[Données non publiées],08/12/1960,Frederique,mostly_female,female
000e41c4-3ae3-46b7-be32-1aa8b74c778b-20171221.xml,24/03/2025 23:24:20,000e41c4-3ae3-46b7-be32-1aa8b74c778b,M.,Gassilloud,Thomas,[Données non publiées],21/05/1981,Thomas,male,male
00138e83-44ec-4da1-89f3-37d2309a62a2-20171221.xml,17/08/2020 19:27:35,00138e83-44ec-4da1-89f3-37d2309a62a2,Mme,SCHMITT,SYLVIE,[Données non publiées],04/04/1964,SYLVIE,female,female
```

## pii/spouse_occupation_gender_counts.csv

**Description:** Counts of spouse occupations split by gender.

**Columns:**

- **occupation** (object)
- **male** (int64)
- **female** (int64)

**Sample (first 5 rows):**

```csv
occupation,male,female
"""Managing Director - Portfolio Performance"" [Donnees Non Publiees]",1,0
"""Market Maker"" (Activite De Trading Algorithmique)",2,0
-,0,2
- Cabinet De Medecine Generale [Donnees Non Publiees],0,1
- Conseillere Departementale De 2015 A 2021. - Vice-Presidente Depuis 2021,0,1
```

## stock_analysis/output/person_stock_sector_report.csv

**Description:** Stock holdings aggregated by GICS sector for each person.

**Columns:**

- **uuid** (object)
- **nom** (object)
- **prenom** (object)
- **GICS Sector** (object)
- **sector_valuation** (int64)
- **total_valuation** (int64)
- **sector_share** (float64)

**Sample (first 5 rows):**

```csv
uuid,nom,prenom,GICS Sector,sector_valuation,total_valuation,sector_share
018db207-7406-48f9-a627-d5455886644e,ASSEH,Bassem,Information Technology,430000,430000,1.0
01e889f4-7c43-4f0a-a8bc-863cf13205cf,briand,philippe,Financials,4964,10977,0.4522182745741095
01e889f4-7c43-4f0a-a8bc-863cf13205cf,briand,philippe,Health Care,2821,10977,0.2569918921381069
01e889f4-7c43-4f0a-a8bc-863cf13205cf,briand,philippe,Information Technology,3192,10977,0.2907898332877836
0260af76-f46a-410b-bea9-265802f921be,ASSEH,Bassem,Information Technology,430000,430000,1.0
```

## stock_analysis/output/indexes/sbf120.csv

**Description:** Stock holdings limited to companies in the SBF120 index.

**Columns:**

- **uuid** (object)
- **nomSociete** (object)
- **evaluation** (int64)
- **capitalDetenu** (float64)
- **nombreParts** (float64)
- **commentaire** (object)
- **remuneration** (object)
- **clean_name** (object)

**Sample (first 5 rows):**

```csv
uuid,nomSociete,evaluation,capitalDetenu,nombreParts,commentaire,remuneration,clean_name
dd0be323-39c8-4f29-9945-760c06b7cd83,Credit agricole SA,110,,15.0,PEA,"10,35",CREDIT AGRICOLE
7bbb60d3-4b7c-4989-bbcd-4141930459f0,Crédit Agricole,748,0.0,53.0,,0,CREDIT AGRICOLE
7bbb60d3-4b7c-4989-bbcd-4141930459f0,ENGIE,741,0.0,46.0,,0,ENGIE
7bbb60d3-4b7c-4989-bbcd-4141930459f0,VEOLIA,888,0.0,30.0,,0,VEOLIA
7bbb60d3-4b7c-4989-bbcd-4141930459f0,Crédit Agricole,40,0.0,2.0,"Il s'agit d'un compte titre sociétaire du Crédit Agricole 
        [Données non publiées]
    ",0,CREDIT AGRICOLE
```

## stock_analysis/output/indexes/sp500.csv

**Description:** Stock holdings limited to companies in the S&P 500 index.

**Columns:**

- **uuid** (object)
- **nomSociete** (object)
- **evaluation** (int64)
- **capitalDetenu** (float64)
- **nombreParts** (float64)
- **commentaire** (object)
- **remuneration** (object)
- **clean_name** (object)

**Sample (first 5 rows):**

```csv
uuid,nomSociete,evaluation,capitalDetenu,nombreParts,commentaire,remuneration,clean_name
92de272e-462a-4ed9-8c8f-2d1bc5fd429b,Accenture,7509,,37.0,"Actions détenues dans le cadre d'un plan d'achat d'actions de mon employeur, Accenture","Dividendes perçus en 2019 : 16,7 US$",ACCENTURE
04dd08d0-c3f9-46a6-a201-7c82b379fd90,Kraft Heinz,440,,6.0,,quelques euros,KRAFT HEINZ
b8f4d483-931f-4e20-9de5-69ec5638ce13,INTEL,21938,6.0,435.0,Pas de dividendes dans l'année précédant la déclaration,0,INTEL
1e9583f0-ef71-490a-9b17-f5cb9c717ead,3M,1188,,7.0,17 en 2020,17,3M
1e9583f0-ef71-490a-9b17-f5cb9c717ead,Colgate-Palmolive,1278,,18.0,9 en 2020,9,COLGATE PALMOLIVE
```

## stock_analysis/output/indexes/cac40.csv

**Description:** Stock holdings limited to companies in the CAC 40 index.

**Columns:**

- **uuid** (object)
- **nomSociete** (object)
- **evaluation** (int64)
- **capitalDetenu** (float64)
- **nombreParts** (float64)
- **commentaire** (object)
- **remuneration** (object)
- **clean_name** (object)

**Sample (first 5 rows):**

```csv
uuid,nomSociete,evaluation,capitalDetenu,nombreParts,commentaire,remuneration,clean_name
dd0be323-39c8-4f29-9945-760c06b7cd83,Credit agricole SA,110,,15.0,PEA,"10,35",CREDIT AGRICOLE
7bbb60d3-4b7c-4989-bbcd-4141930459f0,Crédit Agricole,748,0.0,53.0,,0,CREDIT AGRICOLE
7bbb60d3-4b7c-4989-bbcd-4141930459f0,ENGIE,741,0.0,46.0,,0,ENGIE
7bbb60d3-4b7c-4989-bbcd-4141930459f0,VEOLIA,888,0.0,30.0,,0,VEOLIA
7bbb60d3-4b7c-4989-bbcd-4141930459f0,Crédit Agricole,40,0.0,2.0,"Il s'agit d'un compte titre sociétaire du Crédit Agricole 
        [Données non publiées]
    ",0,CREDIT AGRICOLE
```

## stock_analysis/output/normalized_stocks.csv

**Description:** Normalized stock holdings with GICS sector classifications.

**Columns:**

- **uuid** (object)
- **nomSociete** (object)
- **evaluation** (int64)
- **capitalDetenu** (object)
- **nombreParts** (float64)
- **commentaire** (object)
- **remuneration** (object)
- **clean_name** (object)
- **GICS Sector** (object)
- **GICS Sub-Industry** (object)

**Sample (first 5 rows):**

```csv
uuid,nomSociete,evaluation,capitalDetenu,nombreParts,commentaire,remuneration,clean_name,GICS Sector,GICS Sub-Industry
1debfdad-a34e-4a3f-bbb0-99ef52458e44,SELARL PHARMACIE BATAILLE,847895,54,2760.0,"
        [Données non publiées]
    ",Rémunération de gérance 2020 de 100 999 €.,SELARL PHARMACIE BATAILLE,,
53146fd1-09fe-4e21-b318-d92f0dc10209,ELCO,2000,100,0.0,,0,ELCO,,
53146fd1-09fe-4e21-b318-d92f0dc10209,Cercle des élus locaux,5000,50,0.0,,0,CERCLE DES ELUS LOCAUX,,
a2217ddb-dc26-4efd-b9a1-048d62eac94f,CEIDF Hauts de Seine,200,,10.0,,4 50 €,CEIDF HAUTS DE SEINE,,
dd0be323-39c8-4f29-9945-760c06b7cd83,SARL Rétroscapade,10000,25,100.0,"sans activité. 
        [Données non publiées]
    
        [Données non publiées]
    ",0,SARL RETROSCAPADE,,
```

## stock_analysis/output/person_stock_report.csv

**Description:** Summary statistics of stock portfolios per person.

**Columns:**

- **uuid** (object)
- **nom** (object)
- **prenom** (object)
- **stock_count** (int64)
- **average_valuation** (float64)
- **total_valuation** (int64)
- **min_valuation** (int64)
- **max_valuation** (int64)
- **herfindahl_index** (float64)

**Sample (first 5 rows):**

```csv
uuid,nom,prenom,stock_count,average_valuation,total_valuation,min_valuation,max_valuation,herfindahl_index
01e889f4-7c43-4f0a-a8bc-863cf13205cf,briand,philippe,48,6321978.5625,303454971,0,300000000,0.355104927627046
c2c9d9a9-f982-471c-a314-b2b40f583a93,briand,philippe,48,6321978.5625,303454971,0,300000000,0.355104927627046
4cf9ae19-5c59-42a1-b11a-c976986cc210,PELLENC,ROGER,6,14133609.333333334,84801656,30000,84364000,
f95297b3-1e9a-4d8b-a03b-6d9d3a9a5055,PELLENC,ROGER,1,84364000.0,84364000,84364000,84364000,
a2225105-10a6-4235-a719-52474ea3ba81,COUTIERE,Dominique,2,34473966.0,68947932,44932,68903000,
```

## stock_analysis/index_lists/sbf120.csv

**Description:** List of company names in the SBF120 index.

**Columns:**

- **name** (object)

**Sample (first 5 rows):**

```csv
name
ACCOR
AIR LIQUIDE
AIRBUS
ALSTOM
ARCELORMITTAL
```

## stock_analysis/index_lists/sp500.csv

**Description:** Constituent list of the S&P 500 with sector details.

**Columns:**

- **Symbol** (object)
- **Security** (object)
- **GICS Sector** (object)
- **GICS Sub-Industry** (object)
- **Headquarters Location** (object)
- **Date added** (object)
- **CIK** (int64)
- **Founded** (object)

**Sample (first 5 rows):**

```csv
Symbol,Security,GICS Sector,GICS Sub-Industry,Headquarters Location,Date added,CIK,Founded
MMM,3M,Industrials,Industrial Conglomerates,"Saint Paul, Minnesota",1957-03-04,66740,1902
AOS,A. O. Smith,Industrials,Building Products,"Milwaukee, Wisconsin",2017-07-26,91142,1916
ABT,Abbott Laboratories,Health Care,Health Care Equipment,"North Chicago, Illinois",1957-03-04,1800,1888
ABBV,AbbVie,Health Care,Biotechnology,"North Chicago, Illinois",2012-12-31,1551152,2013 (1888)
ACN,Accenture,Information Technology,IT Consulting & Other Services,"Dublin, Ireland",2011-07-06,1467373,1989
```

## stock_analysis/index_lists/cac40.csv

**Description:** List of company names in the CAC 40 index.

**Columns:**

- **name** (object)

**Sample (first 5 rows):**

```csv
name
ACCOR
AIR LIQUIDE
AIRBUS
ALSTOM
ARCELORMITTAL
```

## stock_extract/stocks.csv

**Description:** Raw extracted stock holdings from declarations.

**Columns:**

- **uuid** (object)
- **nomSociete** (object)
- **evaluation** (int64)
- **capitalDetenu** (object)
- **nombreParts** (float64)
- **commentaire** (object)
- **remuneration** (object)

**Sample (first 5 rows):**

```csv
uuid,nomSociete,evaluation,capitalDetenu,nombreParts,commentaire,remuneration
1debfdad-a34e-4a3f-bbb0-99ef52458e44,SELARL PHARMACIE BATAILLE,847895,54,2760.0,"
        [Données non publiées]
    ",Rémunération de gérance 2020 de 100 999 €.
53146fd1-09fe-4e21-b318-d92f0dc10209,ELCO,2000,100,0.0,,0
53146fd1-09fe-4e21-b318-d92f0dc10209,Cercle des élus locaux,5000,50,0.0,,0
a2217ddb-dc26-4efd-b9a1-048d62eac94f,CEIDF Hauts de Seine,200,,10.0,,4 50 €
a832cde1-4f53-4f31-9379-38d353f1b691,earl [Données non publiées],208240,63,5206.0,valeur vénale de la part 40€,"18000€/an rémunération reprise dans la rubrique 1""activité professionnelle"""
```

## liste.csv

**Description:** Semicolon-separated list of mandates and associated metadata.

**Columns:**

- **civilite** (object)
- **prenom** (object)
- **nom** (object)
- **classement** (object)
- **type_mandat** (object)
- **qualite** (object)
- **type_document** (object)
- **departement** (object)
- **date_publication** (object)
- **date_depot** (object)
- **nom_fichier** (object)
- **url_dossier** (object)
- **open_data** (object)
- **statut_publication** (object)
- **id_origine** (object)
- **url_photo** (object)

**Sample (first 5 rows):**

```csv
civilite;prenom;nom;classement;type_mandat;qualite;type_document;departement;date_publication;date_depot;nom_fichier;url_dossier;open_data;statut_publication;id_origine;url_photo
Mme;Abbassia;HAKEM;hakemaaaabbassia4615;commune;Adjointe au maire de Nantes;di;44;2021-09-27;2020-09-01;hakem-abbassia-di16146-commune-nantes.pdf;/pages_nominatives/hakem-abbassia;hakem-abbassia-di16146-commune-nantes.xml;Livrée;;
Mme;Abbassia;HAKEM;hakemaaaabbassia4615;commune;Adjointe au maire de Nantes;dim;44;2021-09-28;2021-08-02;hakem-abbassia-dim16147-commune-nantes.pdf;/pages_nominatives/hakem-abbassia;hakem-abbassia-dim16147-commune-nantes.xml;Livrée;;
M.;Abdel Kader;CHEKHEMANI;chekhemaniaaaabdelkader1679;commune;Adjoint au maire de Rouen;di;76;2021-10-11;2020-10-14;chekhemani-abdel-kader-di16326-commune-rouen.pdf;/pages_nominatives/chekhemani-abdel-kader;chekhemani-abdel-kader-di16326-commune-rouen.xml;Livrée;;
M.;Abdel Kader;CHEKHEMANI;chekhemaniaaaabdelkader1679;commune;Adjoint au maire de Rouen;dim;76;2021-10-12;2021-07-14;chekhemani-abdel-kader-dim16327-commune-rouen.pdf;/pages_nominatives/chekhemani-abdel-kader;chekhemani-abdel-kader-dim16327-commune-rouen.xml;Livrée;;
M.;Abdelaziz;HAMIDA;HAMIDA Abdelaziz18939;commune;Maire de Goussainville;di;95;2021-08-10;2020-10-03;hamida-abdelaziz-di15206-commune-goussainville.pdf;/pages_nominatives/hamida-abdelaziz-18939;hamida-abdelaziz-di15206-commune-goussainville.xml;Livrée;;
```

## avis/NER/organizations.csv

**Description:** Named organizations extracted via NER.

**Columns:**

- **name** (object)
- **type** (object)

**Sample (first 5 rows):**

```csv
name,type
7SF,Organization
8&,Organization
Adecco Group France,Organization
Afpa,Organization
Anticor,Organization
```

## avis/NER/cleaned_entities.csv

**Description:** Cleaned entity names from NER outputs.

**Columns:**

- **entity** (object)

**Sample (first 5 rows):**

```csv
entity
- Monsieur
- de Monsieur
4 Président
7SF
8&
```

## avis/NER/people.csv

**Description:** Named persons extracted via NER.

**Columns:**

- **name** (object)
- **type** (object)

**Sample (first 5 rows):**

```csv
name,type
Abel,Person
Adrien Caillerez,Person
Adrien Taquet,Person
Agnès Firmin Le Bodo,Person
Agnès Pannier-Runacher,Person
```

## avis/NER/per_entities.csv

**Description:** Mapping between document files and recognized entities.

**Columns:**

- **file** (object)
- **entity** (object)

**Sample (first 5 rows):**

```csv
file,entity
2014-2.txt,n’
2014-21_tif.txt,é Liberté
2014-21_tif.txt,Guillaume Valette-Valla
2014-21_tif.txt,Daniel Lebègue
2014-43.txt,Mme Catherine Bergeal
```

## personal_info_with_gender.csv

**Description:** Personal information with age, gender and first name fields.

**Columns:**

- **file** (object)
- **dateDepot** (object)
- **uuid** (object)
- **civilite** (object)
- **nom** (object)
- **prenom** (object)
- **email** (object)
- **dateNaissance** (object)
- **age** (float64)
- **age_band** (object)
- **first_name** (object)
- **gender_guess** (object)
- **gender** (object)

**Sample (first 5 rows):**

```csv
file,dateDepot,uuid,civilite,nom,prenom,email,dateNaissance,age,age_band,first_name,gender_guess,gender
000765d9-da68-48c6-a95d-f34a12cacb5f-20171221.xml,08/02/2021 19:58:13,000765d9-da68-48c6-a95d-f34a12cacb5f,M.,DELAPORTE,Olivier,[Données non publiées],29/07/1951,69.0,60-69,Olivier,male,male
000b18d0-40c0-4edf-8bf5-e76841fe46df-20171221.xml,18/07/2023 09:47:16,000b18d0-40c0-4edf-8bf5-e76841fe46df,M.,Chaize,Patrick,[Données non publiées],22/03/1963,60.0,60-69,Patrick,male,male
000e2a7c-5fae-4a8d-a1a4-8d04821effc7-20171221.xml,13/01/2025 12:00:37,000e2a7c-5fae-4a8d-a1a4-8d04821effc7,Mme,Meunier,Frederique,[Données non publiées],08/12/1960,64.0,60-69,Frederique,mostly_female,female
000e41c4-3ae3-46b7-be32-1aa8b74c778b-20171221.xml,24/03/2025 23:24:20,000e41c4-3ae3-46b7-be32-1aa8b74c778b,M.,Gassilloud,Thomas,[Données non publiées],21/05/1981,43.0,40-49,Thomas,male,male
00138e83-44ec-4da1-89f3-37d2309a62a2-20171221.xml,17/08/2020 19:27:35,00138e83-44ec-4da1-89f3-37d2309a62a2,Mme,SCHMITT,SYLVIE,[Données non publiées],04/04/1964,56.0,50-59,SYLVIE,female,female
```
