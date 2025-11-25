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


### target_template

Brukes for å fylle inn {{TARGET}} i spørsmål-template og generere forventet stereotype/answer.
