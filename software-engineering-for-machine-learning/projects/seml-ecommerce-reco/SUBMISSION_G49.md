# Group G49 — SEML Assignment I submission

**Architecture chosen for this submission: Event-Driven Architecture + API Gateway.**

The two files to upload to Taxila are in `final_submission/`:

- `final_submission/G49_SEML_Assignment_01_Ecommerce_Recommendation_Final_Report.docx` — the report
- `final_submission/G49.ipynb` — the executable implementation notebook (matches the report)

Supporting, runnable code and evidence: `event_driven_prototype/` (see its `README.md`).

## Two design variants in this repo

This project originally used **Event-Driven Architecture + API Gateway** (the design the report
describes). A later iteration explored **Microservices + CQRS**. Both are kept in
`final_submission/` for reference:

- Event-Driven (submission): `G49.ipynb`, `G49_...Final_Report.docx`
- CQRS (earlier variant): `G049.ipynb`, `G049_...Complete_Report.docx`

The Event-Driven runnable prototype (recovered so the report, notebook, and code all match) is
in `event_driven_prototype/`.

## Before uploading — checklist

- [ ] Fill BITS IDs and names for members 2, 3, 4 (report cover table + notebook first cell).
- [ ] Confirm the final deadline with the group.
- [ ] Run the notebook top-to-bottom (`pip install -r event_driven_prototype/requirements.txt`)
      so its output cells are populated; results are deterministic and match the report.
- [ ] Rename the uploaded files to exactly `G49.ipynb` / `G49.pdf` (or `.docx`) if the
      portal requires the bare group id.
