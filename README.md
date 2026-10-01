# AI Customer Support Agent

An AI support-agent prototype built using AmazonHelp conversations from
the Customer Support on Twitter dataset. It classifies customer intent,
retrieves similar historical conversations, drafts a response, and flags
cases for escalation.

**Status:** Prototype in progress. Response generation is integrated;
evaluation and safety controls remain unfinished.

## What we have done

### Data preparation

-   Inspected 2,811,774 tweets and identified the brands in the dataset.
-   Selected AmazonHelp and filtered 305,008 tweets into
    `data/amazon_help.csv`.
-   Reconstructed conversations using reply and parent-tweet IDs.
-   Cleaned 55,755 reconstructed conversations.
-   Created 55,755 RAG documents.
-   Built and manually labeled a 200-conversation golden set.

### Intent taxonomy

1.  Delivery / Tracking
2.  Order / Pricing
3.  Return / Replacement
4.  Refund
5.  Payment / Billing
6.  Account / Login
7.  Prime Membership
8.  Product / Device
9.  Digital Content
10. Security / Fraud
11. Customer Service / Complaint
12. Other

### Current components

-   **Message filter:** Detects acknowledgements that do not need a
    reply.
-   **Intent classifier:** TF-IDF + Logistic Regression trained on
    golden-set labels.
-   **Retriever:** TF-IDF and cosine similarity over historical
    conversations.
-   **Context builder:** Extracts historical support replies for the
    prompt.
-   **Response generator:** Groq-hosted Llama 3.3 70B drafts a response
    using retrieved context.
-   **Escalation logic:** Keyword rules flag high-risk or potentially
    unresolved cases.
-   **Evaluation:** Intent/escalation evaluation scripts and an LLM
    response judge.

## Architecture

``` mermaid
flowchart TD
    A[Customer message] --> B{Acknowledgement?}
    B -- Yes --> C[Return no-response result]
    B -- No --> D[Intent classifier]
    D --> E[Escalation rules]
    D --> F[TF-IDF retriever]
    F --> G[Similar historical conversations]
    G --> H[Context builder]
    H --> I[LLM response generator]
    A --> I
    E --> J{Escalation required?}
    I --> K[Draft response]
    J --> L[Agent result]
    K --> L
    L --> M[Intent, response, escalation flag and reason]
```

The current prototype can still generate a draft when escalation is
flagged. It does not yet enforce a human-review gate.

## Evaluation so far

### Intent baselines

  Input                       Accuracy   Macro-F1
  ------------------------- ---------- ----------
  Latest customer message        0.175      0.120
  Full conversation              0.350      0.139

These are preliminary results from a small 80/20 split of the
200-example golden set. Performance is uneven across classes, especially
rare intents.

### Escalation

Preliminary results: - Auto-handle: precision 0.62, recall 1.00, F1
0.76 - Escalate: precision 1.00, recall 0.06, F1 0.12 - Accuracy: 0.62;
macro-F1: 0.44

The rules were expanded after reviewing missed cases from this split.
Therefore, these are development results, not an independent final test.

### Response judge

An LLM judge scored five responses from 1--5:

  Example                           Relevance   Groundedness   Helpfulness
  ------------------------------- ----------- -------------- -------------
  Supervisor already contacted              2              4             1
  Delivery left exposed to rain             4              5             3
  Item sold directly by Amazon              5              5             4
  Customer says "Done"                      5              5             5
  Complaint about poor service              2              4             1

This sample is illustrative only. Groundedness should be judged against
retrieved context, not just the customer message.

## Main project structure

``` text
project/
├── data/
│   ├── amazon_help.csv
│   ├── amazon_conversations.csv
│   ├── amazon_conversations_clean.csv
│   ├── amazon_rag_documents.jsonl
│   ├── golden_set.csv
│   ├── agent_evaluation_results.csv
│   └── response_judge_results.csv
└── src/
    ├── agent/
    │   ├── agent.py
    │   ├── intent_classifier.py
    │   ├── escalation.py
    │   └── message_filter.py
    ├── evaluation/
    │   ├── evaluate_baseline.py
    │   ├── evaluate_agent.py
    │   ├── analyze_errors.py
    │   └── response_judge.py
    ├── models/
    │   └── llm.py
    └── rag/
        ├── retriever.py
        ├── build_context.py
        └── generate_response.py
```

This lists the main files used so far, not necessarily every file in the
repository.

## Running the current evaluation

From the project root, with the virtual environment activated:

``` bash
python -m src.evaluation.evaluate_agent
python -m src.evaluation.analyze_errors
python -m src.evaluation.response_judge
```

Response generation requires a local `.env` file containing:

``` env
GROQ_API_KEY=your_api_key_here
```

Do not commit `.env` or API keys.

## What remains

### Evaluation

-   Increase the response-judge sample (for example, to 30 cases).
-   Human-rate the same responses and measure human--LLM agreement.
-   Give the judge retrieved context when scoring groundedness.
-   Create an untouched final test set; use a separate development set
    for tuning.
-   Report per-class precision, recall, F1, support, and a confusion
    matrix.
-   Evaluate retrieval quality and whether retrieved examples contain
    useful resolutions.

### Agent improvements

-   Do not generate/send a customer-facing reply when escalation is
    required; return a handoff result.
-   Improve rare and overlapping intent classification.
-   Use conversation context rather than only one message where
    possible.
-   Add confidence thresholds and a safe fallback for uncertain
    predictions.
-   Improve acknowledgement detection and test short and multilingual
    messages.
-   Require generated claims to be supported by retrieved evidence.

### Final report and delivery

-   Compare two baselines fairly.
-   Analyze the top five failure modes with examples.
-   Explain what is misleading about the headline metric.
-   Record design decisions and limitations.
-   Prepare the report (maximum six pages) and test the repository from
    a clean setup.

## Known limitations and safety

-   Only 200 conversations are labeled, with substantial class
    imbalance.
-   The intent classifier is a simple baseline.
-   Escalation relies on keywords and may miss indirect or
    context-dependent risks.
-   Lexical retrieval can miss semantically similar messages.
-   Historical resolutions may be outdated or inconsistent.
-   The system is not connected to Amazon systems and cannot verify
    orders, refunds, accounts, or delivery status.

Treat generated text as a **draft**. Sensitive, high-risk, unresolved,
or uncertain cases should go to human review. Never claim an action was
completed without verification from an authorized system.
