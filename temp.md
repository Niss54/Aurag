# AuRAG Project Generation Prompts (Chronological Log)

> This document contains the chronological series of 80 developer prompts used to guide the autonomous end-to-end architecture, development, infrastructure provisioning, multi-agent swarming, Lightning Machine Money settlement, and frontend interface for **AuRAG** (Autonomous Industrial RAG & Lightning Settlement Engine).

---

## Phase 1: Repository Scaffolding, Tooling & Infrastructure Baseline (Day 1)

### Prompt 01: Project Inception & Foundation
"Initialize a new repository for AuRAG (Autonomous Industrial RAG & Multi-Agent Swarm with Bitcoin Lightning Settlement). Setup a production-ready `.gitignore` covering Python 3.12, Node.js/Next.js, Neo4j, Qdrant, and environment files. Add an MIT `LICENSE` with copyright Niss54, and create an initial lightweight `README.md` defining our high-level vision: autonomous industrial telemetry diagnostics, multi-agent reasoning, and automated Bitcoin micropayments."

### Prompt 02: Python Dependencies & Testing Manifests
"Create `requirements.txt` and `requirements-dev.txt` for Python 3.12. Include FastAPI, Uvicorn, Pydantic v2, Neo4j driver, Qdrant client, Sentence-Transformers, PyTorch, LangChain/LangGraph primitives, NWC/Nostr libraries, RAGAS, Pytest, and Pytest-asyncio. Also configure `pytest.ini` with custom markers for unit, integration, and e2e test execution."

### Prompt 03: Deterministic Lockfiles
"Generate fully locked requirement files (`requirements.lock` and `requirements-dev.lock`) freezing all sub-dependencies with exact hashes to guarantee reproducible local, CI/CD, and containerized Docker builds."

### Prompt 04: Docker & Multi-Cloud Deployment Manifests
"Write a production multi-stage `Dockerfile` for our backend API and worker processes. Include non-root user execution, cache-optimized pip installs, and healthcheck probes. Add `.dockerignore`, `railway.toml`, and `render.yaml` manifests for instant zero-configuration cloud deployment."

### Prompt 05: Environment Configuration & MCP Schema
"Create `.env.example` and `.env.machine-money.example` detailing all required environment variables: Neo4j credentials, Qdrant endpoints, Redis URL, Gemini/Groq API keys, and Lightning LNbits/NWC connection strings. Also define `mcp_servers.json` for Model Context Protocol integration with local tool registries."

### Prompt 06: Docker Compose Multi-Service Stacks
"Construct `infra/docker-compose.yml` for local development and `infra/docker-compose.prod.yml` for production. Configure services for FastAPI backend, Next.js frontend, Neo4j 5.x enterprise community edition with APOC, Qdrant vector database, and Redis cache with persistent volumes and healthchecks."

### Prompt 07: Neo4j Knowledge Graph Schema & Core Cypher Seeds
"Define the core Neo4j graph schema in `infra/neo4j/schema.cypher` with uniqueness constraints and indexes on `:Equipment(tag)`, `:Document(id)`, `:FailureMode(code)`, and `:Personnel(id)`. Add seed scripts `01_equipment.cypher`, `02_personnel.cypher`, and `03_documents_and_procedures.cypher` modeling industrial chemical plant equipment (centrifugal pumps, heat exchangers, valves)."

### Prompt 08: Neo4j Failure Events & Telemetry Seeds
"Create additional Cypher seed scripts: `04_failure_events.cypher` (historical cavitation, bearing wear, seal leakage logs), `05_work_orders.cypher` (maintenance tickets), `06_regulatory_clauses.cypher` (OSHA/API 610 compliance), and `07_telemetry_signatures.cypher` linking vibration and temperature anomalous baselines to graph nodes."

### Prompt 09: Production Cloud Terraform Modules
"Write reusable AWS Terraform infrastructure modules under `infra/terraform/`: `vpc.tf`, `ecs.tf` (Fargate tasks), `rds.tf` (PostgreSQL), `elasticache.tf` (Redis cluster), `s3.tf` (raw industrial document storage), and `iam.tf` with least-privilege IAM roles and policies."

### Prompt 10: Backend App Package & Modular Layout
"Scaffold the backend Python package under `backend/`. Create `backend/__init__.py`, `backend/requirements.txt`, and initialize the `backend/app/` module with clean package boundaries separating core, db, api, services, and schemas."

---

## Phase 2: Core Backend Architecture, Database & Multi-Tenancy (Day 2)

### Prompt 11: Multi-Tenant Context & JWT Authentication
"Implement `backend/app/core/tenant.py` and `backend/app/core/auth.py`. Support multi-tenant header isolation (`X-Tenant-ID`), JWT bearer token authentication, role-based access control (Operator, Reliability Engineer, Plant Manager), and request context variables for audit trails."

### Prompt 12: Neo4j Async Graph Driver Manager
"Write `backend/app/core/neo4j.py` implementing an asynchronous connection pool manager for Neo4j using `neo4j.AsyncGraphDatabase`. Include automatic reconnects, session context managers, query retry with exponential backoff, and graceful shutdown handlers."

### Prompt 13: Conversation Memory & Session Store
"Create `backend/app/core/memory.py` providing persistent session memory for multi-turn investigative chats. Support Redis-backed chat history with sliding window token pruning, summary compression, and fallback to in-memory dictionary for standalone demo mode."

### Prompt 14: RAGAS Background Evaluation Job Manager
"Implement `backend/app/core/ragas_jobs.py` to manage background asynchronous evaluation jobs. Enable queuing RAGAS metric calculations (faithfulness, answer relevance, context recall) without blocking operator interactive requests."

### Prompt 15: SQLAlchemy Engine & Async Session Factory
"Create `backend/app/db/database.py` with SQLAlchemy async engine, `async_sessionmaker`, and declarative base. Support SQLite for zero-dependency local demo testing and PostgreSQL for enterprise production mode."

### Prompt 16: Relational ORM Models for Audit & Workflows
"Define the relational database ORM models in `backend/app/db/models.py`: `AuditLogEntry`, `WorkOrder`, `IncidentEvent`, `TelemetryAlert`, and `MachinePaymentRecord`. Include foreign keys, indexes on timestamps, and JSON metadata columns."

### Prompt 17: Enterprise Health Diagnostics Service
"Implement `backend/app/services/health.py` and `backend/app/services/__init__.py`. Build comprehensive health diagnostic checks that probe Neo4j graph connectivity, Qdrant vector index status, Redis cache latency, and LLM provider ping, returning structured degradation reports."

### Prompt 18: Cryptographic Audit Logging Service
"Build `backend/app/services/audit.py` implementing an immutable audit trail service. Every user query, agent tool execution, and payment trigger must generate a structured audit entry with SHA-256 integrity hashing and timestamped actor metadata."

### Prompt 19: Automation Rule Engine & Trigger Dispatcher
"Create `backend/app/services/automation.py` containing a rule-based automation engine. Operators can configure automated triggers (e.g. vibration > 7.5 mm/s initiates automated RCA draft and dispatches vendor RFQ)."

### Prompt 20: FastAPI Router & Diagnostic Health Endpoints
"Build `backend/app/api/health.py` exposing `/api/v1/health`, `/api/v1/health/detailed`, and `/api/v1/health/ready`. Provide standard Kubernetes liveness and readiness probe responses with service latency breakdowns."

### Prompt 21: FastAPI Main Application Factory & Middleware
"Create `backend/app/main.py` assembling the FastAPI application. Attach CORS middleware, request ID tracing middleware, exception handlers, and dynamic routing for all v1 API modules. Ensure seamless startup and shutdown lifecycles."

---

## Phase 3: Industrial Ingestion, Multimodal Parsers & Connectors (Day 3)

### Prompt 22: Ingestion Package Architecture & Baseline Benchmarks
"Initialize the `ingestion/` module. Create `ingestion/__init__.py`, `ingestion/requirements.txt`, `ingestion/ground_truth.json`, and `ingestion/extraction_baseline.json` defining precision and recall benchmarks for technical industrial manuals."

### Prompt 23: Text Normalizer & Engineering Symbol Cleaner
"Implement `ingestion/parsers/clean_text.py` and `ingestion/parsers/__init__.py`. Clean OCR noise, normalize engineering units (PSI, bar, RPM, mm/s, gpm), preserve Markdown tables, and strip non-ASCII artifacts from legacy scanned pump manuals."

### Prompt 24: Multimodal OCR Pipeline with Tesseract & Gemini Vision
"Build `ingestion/parsers/ocr.py`. Implement multi-engine OCR extraction: try local Tesseract OCR first for offline speeds, and fall back to Gemini 1.5 Flash Vision for complex degraded scans, stamping extracted text with bounding box coordinates."

### Prompt 25: P&ID Diagram Schematic Parser & Document Quarantine
"Implement `ingestion/parsers/vision_pnid.py`, `ingestion/quarantine.py`, and `ingestion/supersession.py`. Extract piping and instrumentation diagram (P&ID) tag nodes, detect revision stamps, quarantine unparseable documents, and mark outdated SOPs as superseded."

### Prompt 26: Enterprise Document Connector Interfaces
"Create `ingestion/connectors/base.py` defining the abstract `BaseConnector` class with methods `fetch()`, `sync()`, and `get_metadata()`. Implement `ingestion/connectors/sharepoint.py` for enterprise Microsoft 365 SharePoint document sync."

### Prompt 27: SAP-PM & OSIsoft PI Industrial Connectors
"Implement `ingestion/connectors/sap_pm.py` to ingest maintenance work order histories and equipment master records, and `ingestion/connectors/osisoft_pi.py` to pull asset tags, historical alarm logs, and operational setpoints."

### Prompt 28: Quality Management System (QMS) Connector
"Build `ingestion/connectors/qms.py` connecting to regulatory and quality document repositories (ISO 9001 / API 610 compliance records, non-conformance reports, and management-of-change documents)."

### Prompt 29: Gemini Vision Multimodal Utilities & Tag Normalization
"Implement `ingestion/gemini_util.py` and `ingestion/tag_normalizer.py`. Normalize equipment tag variations (e.g. `P-101-A`, `P101A`, `PUMP_101A`) to canonical ISA-5.1 tags and process technical schematics with Gemini Vision structured JSON prompts."

### Prompt 30: Asynchronous Task Workers & Storage Watchers
"Build `ingestion/pipeline.py` and `ingestion/workers/` (`__init__.py`, `storage.py`, `tasks.py`, `watcher.py`). Implement background folder watching, async ingestion queue processing via Redis/Celery, and automatic retry on network failures."

### Prompt 31: Seed Loader, Extraction Accuracy & Ingestion CLI
"Create `ingestion/loader/load_seed.py`, `ingestion/validate_extraction_accuracy.py`, `ingestion/validate_ground_truth.py`, and `ingestion/cli.py`. Provide CLI commands (`python -m ingestion.cli run --dir ./data`) with progress bars and extraction validation scorecards."

---

## Phase 4: Telemetry Streaming, Industrial Adapters & Predictive Intelligence (Day 4)

### Prompt 32: Telemetry Pipeline Architecture & Base Adapters
"Initialize `telemetry/` package. Create `telemetry/__init__.py`, `telemetry/adapters/__init__.py`, and `telemetry/adapters/base.py` defining the `TelemetryAdapter` interface with methods `connect()`, `stream()`, and `disconnect()`."

### Prompt 33: Synthetic SCADA Telemetry Stream Generator
"Build `telemetry/generator.py` and `telemetry/adapters/synthetic.py`. Simulate live sensor readings for centrifugal pumps: vibration RMS, bearing temperature, discharge pressure, suction flow, and motor current, with tunable drift and anomaly injection."

### Prompt 34: OPC-UA Industrial Protocol Adapter
"Implement `telemetry/adapters/opcua.py` to connect directly to industrial PLC/SCADA servers over the OPC Unified Architecture (OPC-UA) binary protocol, reading node variables and mapping them to internal telemetry schemas."

### Prompt 35: NASA IMS Bearing Run-to-Failure Dataset Adapter
"Build `telemetry/adapters/public_dataset.py` and add `telemetry/fixtures/nasa_ims_bearing_sample.json`. Create a reproducible data adapter that replays the real-world NASA IMS bearing run-to-failure vibration dataset to demonstrate authentic predictive wear curves."

### Prompt 36: Frequency Domain Pattern Matcher & FFT Signature Detection
"Create `telemetry/pattern_match.py` and `telemetry/draft.py`. Implement Fast Fourier Transform (FFT) peak detection to identify characteristic mechanical fault frequencies (1X unbalance, 2X misalignment, blade-pass frequency, and high-frequency bearing cage defects)."

### Prompt 37: Predictive Intelligence Engine & RUL Estimator
"Implement `telemetry/predictive_intelligence.py` and `telemetry/validate_telemetry.py`. Calculate Remaining Useful Life (RUL) estimates using exponential degradation models, generate severity scores (NORMAL, WARNING, CRITICAL), and trigger predictive alerts."

### Prompt 38: Background Telemetry Streaming Worker
"Build `telemetry/worker.py` to run an async telemetry consumer service that continuously reads sensor streams, buffers time-series points, triggers pattern matching, and publishes real-time WebSocket events."

### Prompt 39: Ingestion & Connector REST APIs
"Create `backend/app/api/ingestion.py` and `backend/app/api/connectors.py` exposing REST endpoints for uploading documents, triggering ingestion pipelines, checking extraction progress, and testing external enterprise connectors."

### Prompt 40: Real-Time Telemetry REST & SSE Endpoints
"Implement `backend/app/api/telemetry.py` providing endpoints to query live telemetry buffers, fetch time-series historical charts, stream Server-Sent Events (SSE) for sensor anomalies, and manage alert thresholds."

### Prompt 41: Equipment Registry & Knowledge Risk APIs
"Build `backend/app/api/equipment.py`, `backend/app/api/knowledge_risk.py`, and `backend/app/services/knowledge_risk.py`. Analyze tribal knowledge risk (un-documented procedures, single-engineer dependencies, retiring personnel) using graph centralities."

### Prompt 42: Work Orders & Historical Incident APIs
"Implement `backend/app/api/work_orders.py`, `backend/app/api/events.py`, `backend/app/services/work_orders.py`, and `backend/app/services/events.py`. Provide endpoints for creating, updating, and querying maintenance work orders linked to graph failure events."

### Prompt 43: Synthetic Test Dataset & P&ID Schematics
"Create the demo dataset in `data/`: `data/SOURCES.md`, `data/documents/incident_log.md`, `data/documents/pump_pm_sop.md`, `data/pnid/sample_pnid.pdf`, and `data/scanned/scnd1.jpeg` representing authentic plant documentation."

---

## Phase 5: Hybrid Retrieval, Vector/Graph Search & Multi-Vendor Services (Day 5)

### Prompt 44: Retrieval Engine Architecture & Ground Truth Specs
"Initialize the `retrieval/` package. Create `retrieval/__init__.py`, `retrieval/requirements.txt`, and `retrieval/ground_truth.json` defining 50 benchmark industrial retrieval queries with exact chunk IDs for evaluation."

### Prompt 45: Dense Embeddings Abstraction Layer
"Implement `retrieval/embeddings.py`. Build a unified embedding wrapper supporting local HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (for zero-latency offline mode) and OpenAI `text-embedding-3-small` with automatic batching and vector caching."

### Prompt 46: Qdrant Vector Store Indexer & Search Client
"Create `retrieval/qdrant_store.py` and `retrieval/plain_vector.py`. Implement Qdrant collection setup with Cosine distance, payload indexing for tenant ID and equipment tag filters, and cosine similarity k-NN search."

### Prompt 47: BM25 Sparse Keyword Retrieval Index
"Implement `retrieval/bm25_index.py` using `rank-bm25`. Build an in-memory sparse keyword index tokenized with engineering stopword filtering to ensure exact alphanumeric tag matches (e.g. `P-101A`, `ISO-2858`) aren't lost in dense vector search."

### Prompt 48: Neo4j Knowledge Graph Traversal & Multi-Hop Querying
"Create `retrieval/graph_traversal.py` and `retrieval/selfcheck_neo4j_vector.py`. Implement multi-hop Cypher queries that start from an equipment node and traverse relationships (`:HAS_FAILURE_MODE`, `:DESCRIBED_IN`, `:REQUIRES_SOP`, `:MAINTAINED_BY`) to extract connected graph context."

### Prompt 49: Hybrid Reciprocal Rank Fusion (RRF) & Candidate Filtering
"Implement `retrieval/hybrid.py` and `retrieval/candidate_filter.py`. Combine dense vector search, BM25 sparse keyword search, and Neo4j graph context using Reciprocal Rank Fusion (RRF) with configurable weights ($k=60$) and deduplication."

### Prompt 50: Cross-Encoder Contextual Reranking
"Create `retrieval/rerank.py` and `retrieval/index_chunks.py`. Implement a secondary reranker using `cross-encoder/ms-marco-MiniLM-L-6-v2` (with fallback to LLM scoring) to score query-document pairs, boosting top precision and filtering irrelevance."

### Prompt 51: Real Corpus Ingestion & Retrieval Validator Harness
"Build `retrieval/ingest_real_corpus.py` and `retrieval/validate_retrieval.py`. Provide scripts to index technical manuals into Qdrant and Neo4j and compute Mean Reciprocal Rank (MRR@5) and Recall@10 across the ground truth benchmark."

### Prompt 52: Vendor Microservices (Apex, Precision, Quantum)
"Build synthetic vendor API services under `services/`: `services/vendor_apex/server.py` (expedited mechanical seals), `services/vendor_precision/server.py` (vibration analysis specialists), and `services/vendor_quantum/server.py` (OEM pump overhauls) with webhook endpoints."

### Prompt 53: Vendor Management & Knowledge Graph APIs
"Implement `backend/app/api/vendors.py` and `backend/app/api/graph.py`. Expose endpoints for listing vendor capabilities, testing webhooks, and returning interactive nodes/edges JSON for knowledge graph visualization."

### Prompt 54: Automated Trigger Engine & Comparative Analysis Endpoints
"Build `backend/app/api/automations.py`, `backend/app/api/comparison.py`, and `backend/app/services/comparison.py` comparing Plain RAG vs Graph RAG vs Hybrid RAG performance, latency, and context precision."

---

## Phase 6: Multi-Agent Swarm, Safety Guardrails & Copilot (Day 6)

### Prompt 55: Multi-Agent Swarm Architecture & Query Benchmarks
"Initialize `agents/` module. Create `agents/__init__.py`, `agents/requirements.txt`, `agents/ground_truth.json`, and `agents/ambiguous_queries.json` defining test cases for multi-agent reasoning, ambiguous query disambiguation, and safety verification."

### Prompt 56: Shared Agent Blackboard State Schema
"Implement `agents/state.py` and `agents/util.py`. Define the shared agent state dataclass (`AgentState`) containing user query, retrieved context, hypothesis list, verified claims, citation map, token budget, and execution logs."

### Prompt 57: LLM Provider Router & Model Agnostic Client
"Build `agents/llm.py` providing a robust provider-agnostic interface with fallbacks across Groq (Llama-3.3-70B), Google Gemini (Gemini 1.5 Pro/Flash), and local Ollama models with temperature control and structured JSON schema parsing."

### Prompt 58: Industrial Safety Guardrails & Prompt Injection Defense
"Implement `agents/guardrails.py`. Build input/output safety guardrails: detect prompt injection attacks, sanitize system instruction overrides, verify engineering boundary conditions (e.g. pressure cannot be negative), and block unsafe recommendations."

### Prompt 59: Dynamic Citation Resolver with Anchor Verification
"Build `agents/citation_resolver.py`. Verify that every factual claim in the generated response directly cites a retrieved chunk ID or graph entity. Strip unanchored hallucinations and assign confidence scores."

### Prompt 60: Regulatory Compliance Agent & Safety Rule Packs
"Create `agents/compliance.py` and `agents/compliance_packs.py`. Implement a compliance specialist agent that cross-checks proposed maintenance actions against OSHA 1910.119 (Process Safety Management) and API 610 standards."

### Prompt 61: Root Cause Analysis (RCA) 5-Why Specialist Agent
"Implement `agents/rca.py`. Build an autonomous RCA agent that applies the 5-Why methodology and Ishikawa (Fishbone) diagram structures to synthesize telemetry data, maintenance history, and operator logs into root causes."

### Prompt 62: Historical Lessons Learned Extraction Agent
"Build `agents/lessons_learned.py`. Implement an agent that searches past failure post-mortems and incident logs, extracting actionable preventive measures and past operator mistakes."

### Prompt 63: Supervisory Agent & Interactive Engineering Copilot
"Create `agents/supervisor.py` and `agents/copilot.py`. Implement the central supervisor that plans execution steps, routes tasks to specialized agents (Retriever, RCA, Compliance), reviews findings, and provides real-time streaming copilot responses."

### Prompt 64: Unified Agent Gateway & Model Context Protocol Config
"Build `agents/gateway.py`, `agents/validation.py`, `agents/validate_agents.py`, and `agents/validate_supervisor.py`. Add `.agents/mcp_config.json` and `.cursor/mcp.json` exposing the multi-agent swarm tools via MCP standard."

### Prompt 65: Conversational RAG Streaming Chat REST API
"Implement `backend/app/api/chat.py` exposing `/api/v1/chat` and `/api/v1/chat/stream`. Stream multi-agent thinking tokens, reasoning steps, tool invocation notifications, and final markdown answers over SSE."

---

## Phase 7: Bitcoin Lightning & Machine Money Settlement Protocol (Day 7)

### Prompt 66: Machine Money Protocol Schemas & Exception Types
"Initialize `backend/app/services/machine_money/` (`__init__.py`, `schemas.py`, `exceptions.py`). Define Pydantic models for `Invoice`, `PaymentQuote`, `PaymentProof`, `RFQBid`, `VendorQuote`, and custom exceptions for budget exhaustion and policy violations."

### Prompt 67: BOLT11 Invoice Parsing & Preimage Validation Engine
"Implement `backend/app/services/machine_money/bolt11.py`. Decode BOLT11 Lightning payment request strings (human-readable part, payment hash, amount in satoshis, expiry, route hints) without external daemon dependencies."

### Prompt 68: Payment Provider Base Abstraction & Mock Provider
"Create `backend/app/services/machine_money/providers/` (`__init__.py`, `base.py`, `mock.py`). Define `BaseLightningProvider` and implement `MockLightningProvider` that generates simulated BOLT11 invoices and settles with authentic SHA-256 preimages for testing."

### Prompt 69: LNbits & Nostr Wallet Connect (NWC) Provider Adapters
"Implement `backend/app/services/machine_money/providers/lnbits.py`, `providers/nwc.py`, and `providers/factory.py`. Connect to live LNbits API endpoints and Nostr relays to create and pay real Lightning invoices."

### Prompt 70: NIP-47 Nostr Wallet Connect (NWC) Transport Client
"Build `backend/app/services/machine_money/nwc.py`. Implement the NIP-47 Nostr protocol: parse `nostr+walletconnect://` URIs, compute shared secrets via secp256k1 ECDH, encrypt payloads with AES-256-CBC, and send `pay_invoice` commands over Nostr relays."

### Prompt 71: Vendor Service Discovery Registry
"Create `backend/app/services/machine_money/registry.py`. Maintain an active registry of certified industrial vendors (Apex, Precision, Quantum) with public keys, Lightning addresses, SLA ratings, and webhook endpoints."

### Prompt 72: Autonomous RFQ Auction Negotiation Pipeline
"Implement `backend/app/services/machine_money/rfq.py`. When an anomaly occurs, broadcast a Request for Quote (RFQ) to registered vendors, score their returned bids using weighted criteria (50% Cost + 30% Latency + 20% SLA), and select the winning quote."

### Prompt 73: Dynamic Fee Routing & Industrial Economics Engine
"Build `backend/app/services/machine_money/routing.py` and `backend/app/services/machine_money/economics.py`. Calculate payment routing fees and model unplanned downtime exposure ($1.17M modeled exposure based on 7.8M:1 exposure-to-payment ratio)."

### Prompt 74: Cryptographic Proof Grounding & Settlement Bridge
"Implement `backend/app/services/machine_money/grounding.py`, `graph.py`, and `bridge.py`. Verify that `SHA256(preimage) === payment_hash`, record the settlement on the Neo4j graph, and update the associated work order status to `SETTLED`."

### Prompt 75: Machine Money Core Service & Analytics Stream
"Build `backend/app/services/machine_money/service.py` and `backend/app/services/machine_money/analytics.py`. Enforce hard per-transaction spending caps (500 sats), daily budget ceilings (250k sats), SHA-256 idempotency caching, and compute live settlement metrics."

### Prompt 76: Machine Money REST API Endpoints
"Implement `backend/app/api/machine_money.py` exposing endpoints: `/api/v1/machine-money/rfq/request`, `/api/v1/machine-money/quote/approve`, `/api/v1/machine-money/pay`, `/api/v1/machine-money/history`, and `/api/v1/machine-money/stats`."

---

## Phase 8: Frontend Next.js 15 UI, Comprehensive Tests & Production Release (Day 8)

### Prompt 77: RAGAS Benchmark Suite & Evaluation API
"Implement `evaluation/` (`__init__.py`, `requirements.txt`, `benchmark_50.json`, `score.py`, `run_benchmark.py`, `validate_comparison.py`, `validate_ragas.py`) and `backend/app/api/evaluations.py`. Run automated benchmark evaluation across 24 test queries."

### Prompt 78: Next.js 15 Project Setup with TypeScript & Tailwind CSS
"Initialize the frontend application under `frontend/` using Next.js 15 App Router, TypeScript, and Tailwind CSS. Setup `package.json`, `tsconfig.json`, `next.config.ts`, `postcss.config.mjs`, `eslint.config.mjs`, and `components.json`."

### Prompt 79: UI Foundations, Cryptographic Session & Live Event Hooks
"Create `frontend/app/globals.css`, `frontend/lib/utils.ts`, `frontend/lib/api.ts`, `frontend/lib/crypto.ts` (Web Crypto API SHA-256 verification), `frontend/lib/session.ts`, `frontend/hooks/use-mobile.ts`, and `frontend/hooks/use-live-events.ts`."

### Prompt 80: Shadcn UI Atomic Primitive Component Library
"Implement Shadcn UI primitive components under `frontend/components/ui/`: `alert.tsx`, `badge.tsx`, `breadcrumb.tsx`, `button.tsx`, `card.tsx`, `empty.tsx`, `field.tsx`, `input.tsx`, `scroll-area.tsx`, `select.tsx`, `separator.tsx`, `sheet.tsx`, `sidebar.tsx`, `skeleton.tsx`, `tabs.tsx`, `textarea.tsx`, `tooltip.tsx`."

### Prompt 81: Application Shell, Sidebar Navigation & Telemetry Panels
"Build `frontend/components/AppShell.tsx`, `frontend/components/AppSidebar.tsx`, `frontend/components/DashboardHeader.tsx`, `frontend/components/ChatPanel.tsx`, `frontend/components/GraphCanvas.tsx`, `frontend/components/GraphPanel.tsx`, and `frontend/components/TelemetryPanel.tsx`."

### Prompt 82: Operational Domain Dashboards
"Implement dashboard components: `frontend/components/comparison/ComparisonWorkspace.tsx` (Plain vs Graph vs Hybrid RAG), `frontend/components/knowledge-risk/KnowledgeRiskView.tsx`, `frontend/components/evaluation/EvaluationDashboard.tsx`, and `frontend/components/work-orders/WorkOrderEditor.tsx`."

### Prompt 83: Machine Money Lightning Settlement & RFQ Trading UI
"Build `frontend/components/machine-money/`: `Bolt11QRCode.tsx`, `EvidenceSummaryCard.tsx`, `ExecutionTimeline.tsx`, `IndustrialEconomics.tsx`, `JudgeMode.tsx`, `NovelBitcoinProtocol.tsx`, `PaymentProofDrawer.tsx`, `ProofVerification.tsx`, `SystemReadinessModal.tsx`, and `VendorRFQ.tsx`."

### Prompt 84: Next.js App Routes, Screenshots & E2E Test Setup
"Implement Next.js app pages under `frontend/app/`: `page.tsx` (Command Center), `predictive-watch/page.tsx`, `investigate/page.tsx`, `machine-money/page.tsx`, `comparison/page.tsx`, `knowledge-risk/page.tsx`, and configure `playwright.config.ts` and `vitest.config.ts`."

### Prompt 85: Comprehensive Backend & Integration Test Suite
"Write unit and integration test suites in `tests/`: `tests/test_bolt11.py`, `tests/test_nwc_nip47.py`, `tests/test_machine_money_rfq.py`, `tests/test_machine_money_idempotency.py`, `tests/test_e2e_machine_money.py`, and `tests/test_secret_scan.py` ensuring zero API key leaks."

### Prompt 86: Operational Scripts & Disaster Recovery Drills
"Create administrative scripts in `scripts/`: `scripts/backup_restore.py`, `scripts/disaster_recovery_drill.py`, `scripts/health_probe.py`, `scripts/secret_scan.py`, `scripts/validate_mem0.py`, and `scripts/bootstrap.ps1`."

### Prompt 87: Architectural Specifications & Hacker House Goa Guides
"Write technical documentation: `ARCHITECTURE.md`, `JUDGE_README.md`, `docs/HHGOA_SUBMISSION.md`, `docs/HHGOA_MACHINE_MONEY_DEMO.md`, `docs/HACKATHON_ELIGIBILITY.md`, `docs/PRD.md`, and `docs/CLAIM_EVIDENCE_MATRIX.md`."

### Prompt 88: Final Production Release & Comprehensive Readme
"Finalize `README.md` with complete architecture diagrams, live demo steps, ASCII system workflows, security threat models, RAGAS benchmark tables, and MIT licensing for Hacker House Goa release."
