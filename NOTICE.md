# NOTICE: This is a fictional demonstration system

## Meridian John Doe Financial does not exist

**Meridian John Doe Financial** (brand short form **Meridian J.D.**) is a wholly fictional company invented for this portfolio project. The name deliberately contains "John Doe" to make its fictional nature unmistakable.

Everything in this repository is synthetic:

- The company, its departments, executives, and employees are invented.
- Every policy, standard, procedure, runbook, and guideline in `corpus/` is fabricated for demonstration. None of it is real institutional policy from any organization.
- All names, account numbers, identifiers, SSNs, transaction figures, and personal data are fake and clearly marked as test data.
- Regulatory references (BSA, OFAC, SR 11-7, GLBA, PCI DSS, Basel III, and similar) name real frameworks, but every interpretation, threshold, and procedure built around them here is synthetic and must not be used as compliance guidance.

## Intentionally planted test content

For security and evaluation testing, the corpus contains clearly scoped planted artifacts:

- A **prompt-injection canary** (a document line that attempts to manipulate an AI assistant). The system is built and tested to ignore it.
- A **synthetic-PII canary** (fabricated personal data in a marked test record). Used to verify PII never leaks into logs or output.
- A **near-duplicate superseded pair** (the same procedure at two effective dates). Used to verify version handling.

These are not bugs. They are test fixtures.

## Do not use as real-world guidance

Nothing here is legal, financial, security, or compliance advice. This repository exists to demonstrate enterprise AI engineering practice (retrieval-time access control, RAG self-threat-modeling, and quantitative evaluation), not to encode any real institution's controls.
