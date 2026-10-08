# 📦 Historical Archive: Autonomous Machine Money Protocol (Bitcoin Lightning)

> **Document Status:** Archived Historical Specification & Experimental Track  
> **Original Track:** Autonomous Machine Money & Cyber-Physical Settlement  
> **Event:** Hacker House Goa (HHGoa) 2026  
> **Preserved For:** Architectural completeness, audit trail, and historical provenance.

---

## 1. Executive Summary of Archived Research

During earlier hackathon architectural phases, AuRAG explored an experimental cyber-physical economic extension: **Autonomous Machine Money**.

The core premise investigated:
* Industrial unplanned downtime costs an estimated **$22,000 per minute**.
* Traditional enterprise procurement and field service dispatch often take hours or days due to manual paperwork and human purchase order approvals.
* Physical plant assets (e.g., pumps, turbines, compressors) cannot open traditional bank accounts or hold credit cards.
* The module explored whether autonomous industrial machines could hold sovereign Bitcoin Lightning Network wallets to settle micro-diagnostic compute fees (e.g., 250 satoshis / ~$0.15) with external edge AI diagnostic providers.

---

## 2. Key Technical Concepts Explored

1. **Deterministic Expenditure Justification via GraphRAG**:
   * A sensor alert detects a physical vibration anomaly (e.g., NASA IMS bearing 5.42 mm/s breaching ISO-10816 Zone C).
   * Before releasing any payment, the Neo4j knowledge graph verifies active work orders (`WO-1002`), operating procedures (`PROC-001`), and warranty coverage.
2. **Zero-Trust Spending Policy Escrow**:
   * A hard spending limit of **500 satoshis (~$0.30)** was enforced.
   * Micro-diagnostic bids ≤ 500 sats were authorized automatically; any expenditure > 500 sats required human cryptographic operator sign-off.
3. **BOLT11 Invoicing & Cryptographic Preimages**:
   * Synthetic and live BOLT11 payment requests were decoded to extract satoshi amounts and payment hashes.
   * Settlement verification was locked via SHA-256 preimages (`SHA256(preimage) == payment_hash`).
   * Proven settlements were anchored directly back into the Neo4j operational graph: `(Payment)-[:FUNDS]->(WorkOrder)`.
4. **Transport Adapters (LNbits & NIP-47 NWC)**:
   * LNbits API provider adapter.
   * NIP-47 Nostr Wallet Connect (NWC) relay client for encrypted command dispatch.
   * Deterministic mock provider for offline hackathon demonstration stability.

---

## 3. Related Archived Documents

For deep-dive technical reviews of this historical exploration, refer to:
* [**ARCHITECTURE_MACHINE_MONEY.md**](../ARCHITECTURE_MACHINE_MONEY.md): Detailed protocol specifications.
* [**MACHINE_MONEY_VERIFICATION.md**](../MACHINE_MONEY_VERIFICATION.md): Verification report and test suites.
* [**HHGOA_MACHINE_MONEY_DEMO.md**](../HHGOA_MACHINE_MONEY_DEMO.md): 3-minute video presentation storyboard and script.
* [**MACHINE_MONEY_ACCEPTANCE.md**](./MACHINE_MONEY_ACCEPTANCE.md): Acceptance testing checklist.

---

*This document is maintained strictly as an archival reference. The primary submission for Hacker House Goa 2026 shortlisting is focused on **Voice-Driven Development Evidence via Wispr Flow** and **Industrial GraphRAG Knowledge Intelligence**.*
