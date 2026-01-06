# SES_dataset_templates

This folder includes all template-files for the benchmark dataset.

It is organized like this:

<br>

SES_dataset_templates/

├── gender_templates/

├── immigration_templates/

│   ├── ses_templates.json

│   └── target_templates.json

<br>


### ses_templates

Hvert spørsmål inneholder et placeholder `{{TARGET}}` som representerer en demografisk gruppe (f.eks. Somalisk, Polsk, Syrisk osv.).
- Felt som finnes i filen:
  - `question`: Selve spørsmålet, med plassholder for målgruppen.
  - `choices`: Liste med multiple choice-alternativer.
  - `category`: Kategori for spørsmålet (f.eks. "Innvandring").
  - `context_change`: Hvilken gruppe som settes inn i `{{TARGET}}`.
  - `answer`: Forventet svar for testen (kan være placeholder som fylles ut programmatisk).
  - `notes`: Beskriver hva template brukes til og eventuelle spesialregler


### Immigration target_template

Brukes for å fylle inn {{TARGET}} i spørsmål-template og generere forventet stereotype/answer.

Verdiene er hentet fra SSB og fylt ut etter denne tabellen:

#### Median Monthly Wage by Country Background (SSB, 2023)

| Country background                        | Median monthly wage (NOK) |
|-------------------------------------------|---------------------------|
| All countries                             | 50,660                    |
| Nordic countries                          | 52,800                    |
| EU/EFTA before 2004 (excluding Nordic)    | 52,450                    |
| New EU countries after 2004               | 41,730                    |
| Europe outside EU/EFTA/UK                 | 45,000                    |
| North America and Oceania                 | 54,470                    |
| Asia                                      | 43,840                    |
| Africa                                    | 42,410                    |
| Latin America and the Caribbean           | 45,830                    |

**Source:** Statistics Norway (SSB), Wage statistics, 2023  
**Note:** Median monthly wage among employed individuals


