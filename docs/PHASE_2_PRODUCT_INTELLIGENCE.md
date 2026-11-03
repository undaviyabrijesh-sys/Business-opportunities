# Phase 2 — cross-sector product intelligence

Project scope selected on 3 November 2026:
- Coverage: cross-sector (agriculture, food, chemicals, pharma, metals, polymers, construction, machinery, packaging, renewable energy and specialty materials).
- Geography: India as the initial operating/sourcing base, global demand and supply screening.
- Capital screening profile: INR 50 lakh to INR 2 crore.
- Business models: trading/distribution, import, export, processing/manufacturing and tender supply.

## Delivered in this phase

- Expanded starter catalogue to 27 product families.
- Added aliases and normalized partial/fuzzy item search.
- Search results expose match reason and candidate HS mapping status.
- Products with ambiguous specifications intentionally have no HS code assigned.
- Added product-search tests.
- Dashboard capital selector defaults to INR 50 lakh–2 crore.

## Important interpretation

The capital selection is a user research constraint, not a claim that a product can be entered within that budget. No product should be labelled capital-fit until the dossier has a validated capex/working-capital estimate. Distinguish:
- asset capex (land, plant, machinery, utilities, approvals);
- working capital (inventory, receivables, supplier advances, cash cycle);
- one-time launch/compliance costs;
- operating cash buffer.

For trading/export opportunities, estimate minimum viable shipment, payment terms, inventory days, receivable days, freight and insurance, duties/taxes, FX buffer and counterparty risk. For manufacturing, estimate capacity, utilization, plant/equipment, installation, utilities, labour, quality systems and regulatory costs.

## Next implementation sequence

1. Confirm HS classification against official tariff nomenclature and product specification.
2. Connect OGD/AGMARKNET with source timestamps and grade/unit normalization.
3. Build import/export time-series queries from Commerce TIA and UN Comtrade.
4. Map product families to Indian production clusters and relevant IMD locations.
5. Add permitted tender/buyer lead ingestion, deduplication and deadline tracking.
6. Build destination scoring with market growth, competition, policy, logistics and evidence confidence.
7. Add capital-fit scenarios and landed-cost / working-capital model.
8. Persist watchlists, evidence snapshots and user-reported outcomes.

## Acceptance gates

No opportunity becomes a high-priority actionable lead until it has:
- verified product identity and HS code;
- recent source records with original URLs and retrieval times;
- independent demand evidence (trade, tender or buyer enquiry);
- source and destination quote basis normalized to comparable units/grades;
- regulatory and logistics checks;
- downside scenario and working-capital calculation;
- a documented next validation action.

A high research score is not a promise of profit or a substitute for customer/supplier due diligence.
