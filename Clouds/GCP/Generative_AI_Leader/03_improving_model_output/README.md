# Module 3: Improving Generative AI Model Output

## Why This Topic Matters for Business Leaders
Deploying a foundation model out of the box is rarely enough. The same underlying model can deliver dramatically different results depending on how it is configured, what information it has access to, how it is instructed, and how its outputs are governed after deployment.

Organizations that understand how to improve model output get significantly more value from their AI investments. Those that do not often find themselves frustrated by hallucinations, generic responses, inconsistent quality, and eroding trust among the employees and customers who use AI-powered tools.

This module covers the toolkit for improving AI output — from the lightweight techniques we can implement in hours to the more substantial approaches that require engineering investment, and the ongoing monitoring work that never stops.

---

## The Core Problem: Foundation Models Have Real Limitations
Foundation models like Google's Gemini are remarkable achievements. A single model can write, summarize, translate, reason, code, and converse across virtually any topic. But this general-purpose capability comes with inherent limitations that every organization deploying AI must understand.

**A foundation model does not know our organization.** It knows the general concept of insurance, but not our specific insurance products. It knows how customer service works in general, but not the specific policies, tone, and escalation paths our company uses. It can reason about regulatory compliance broadly, but not about the specific regulations that apply to our industry and jurisdiction.

**A foundation model's knowledge has a cutoff date.** Its training data ends at a specific point in time. Events, product launches, regulatory changes, and market developments after that date are unknown to it.

**A foundation model generates, it does not verify.** This is the root cause of hallucination. The model produces text that is statistically consistent with its training — which usually produces accurate, useful content, but occasionally produces confident-sounding falsehoods.

**A foundation model reflects patterns in its training data, including biases.** If the training data reflects historical patterns that encode unfair or inaccurate assumptions, the model may reproduce those patterns.

Understanding these limitations is the prerequisite to solving them.

---

## The Improvement Toolkit
Organizations have a range of techniques available to address foundation model limitations. They differ significantly in effort, cost, and the types of problems they solve best. Choosing the right technique — or the right combination — for our situation is one of the most important decisions in AI deployment.

### Lightweight Techniques
**Prompt Engineering** is the practice of designing the instructions we give the model to elicit better, more accurate, and more consistently useful responses. It requires no changes to the model itself, no data infrastructure, and no model training. It is the starting point for almost every AI deployment — and it is more powerful than many leaders realize. A poorly constructed prompt and a well-crafted prompt given to the same model can produce outputs that are orders of magnitude apart in quality and usefulness.

Good prompt engineering is a skill our organization can develop and systematize. Effective prompts become organizational assets — reusable templates that any team member can apply to recurring tasks.

### Grounding and Knowledge Access
**Grounding** connects the model's responses to specific, verified information sources rather than relying solely on training knowledge. Instead of answering from memory, a grounded model consults authoritative sources — our internal knowledge base, real-time web search, or curated external data — before generating a response.

**Retrieval-Augmented Generation (RAG)** is the most widely used grounding architecture. It pairs the model with a searchable knowledge base: relevant documents are retrieved in response to each query and provided to the model as context. This dramatically reduces hallucination for organizational knowledge questions, keeps information current without retraining the model, and provides traceability — we can see which source documents informed each response.

RAG is usually the most practical and cost-effective approach for making a general AI model knowledgeable about our specific organization.

### Sampling Parameter Control
Beyond what we tell the model, how the model generates its output is controlled by a set of parameters. **Temperature** controls how creative versus predictable the model's responses are — a critical setting that most AI tools expose but few users understand deeply. **Top-P** (nucleus sampling) controls which words the model considers at each step. **Token limits** control output length and manage cost. **Safety settings** control what content the model will generate or engage with.

Understanding these parameters allows us to tune model behavior for our specific use case — precision and consistency for factual applications, more creativity for generative tasks, appropriate length for the interface.

### Heavier Investment Approaches
**Fine-Tuning** involves additional training of the model on domain-specific data. Unlike prompting and grounding — which work at inference time — fine-tuning changes the model itself, making it intrinsically better at specific tasks in specific domains. The analogy used in this guide's other modules is apt: fine-tuning is like giving a well-educated new hire an intensive onboarding program in our company's specific domain. They already have broad knowledge; fine-tuning sharpens their performance for our context.

Fine-tuning is more expensive, slower to implement, and requires more technical expertise than prompting or RAG. It is the right choice when the model needs to deeply internalize a domain, when style and format consistency are critical and cannot be achieved through prompting, or when RAG has been tried and found insufficient.

### Human Oversight
**Human in the Loop (HITL)** is not a technical technique — it is an architectural and process decision. It means designing workflows so that human beings review, validate, or approve AI outputs before consequential actions are taken on them. HITL is essential for high-stakes decisions: hiring, medical triage, legal advice, financial actions, communications to customers in sensitive situations.

As AI capabilities improve, the point at which humans intervene can move later in the workflow — but for anything with significant consequences if wrong, human oversight remains an essential safeguard.

---

## The Techniques Along a Spectrum
It helps to think of these techniques as a spectrum from lightweight to heavyweight:

| Technique | What Changes | Effort | Best For |
|-----------|-------------|--------|----------|
| Prompt Engineering | Nothing — only how we instruct the model | Low | Improving output quality, consistency, and format |
| Sampling Parameters | Model generation behavior at runtime | Very Low | Controlling creativity, length, safety |
| Grounding / RAG | What information the model can access | Medium | Organizational knowledge, current information, reducing hallucination |
| Fine-Tuning | The model itself, via additional training | High | Deep domain expertise, style consistency, specialized tasks |
| HITL | The surrounding workflow and process | Varies | High-stakes decisions, trust-building, regulatory requirements |

Most organizations use multiple techniques together. A well-designed customer service AI, for example, might combine: carefully engineered system prompts, RAG against the company's support knowledge base, low temperature for consistency, and human escalation paths for sensitive issues.

---

## Why Monitoring Matters — Not Just During Development
A common mistake in AI deployment is treating monitoring as a development activity that ends when the model goes live. In reality, monitoring is ongoing work that never stops.

Models can degrade in performance as the world changes and the distribution of inputs shifts from what was expected. A model trained on customer questions from 2023 may perform differently on the questions customers ask in 2025 after a product line change. A model grounded in a knowledge base that has not been updated becomes progressively less accurate over time. A model deployed without performance tracking will fail silently — users will stop trusting it without anyone in the AI team knowing why.

Google Cloud also automatically updates underlying models to maintain security and performance. These updates can change model behavior — sometimes improving it, occasionally changing outputs in ways that affect consistency. Organizations need processes to test before new model versions are rolled out to production users.

**Continuous monitoring is as essential as deployment.** It includes tracking model performance against defined KPIs, monitoring for output drift, maintaining the knowledge bases that support RAG, testing before model version updates, and maintaining security patches.

---

## Topics in This Section
This module contains three detailed files that cover each area of improvement in depth:

- **[3.1 Foundation Model Limitations](./3.1_foundation_model_limitations.md)**: What the limitations are, why they exist, what they look like in practice, and the full Google Cloud toolkit for addressing them — including grounding, RAG, fine-tuning, HITL, and continuous monitoring practices.

- **[3.2 Prompt Engineering Techniques](./3.2_prompt_engineering_techniques.md)**: A comprehensive deep-dive on prompt engineering — zero-shot, one-shot, few-shot, role prompting, prompt chaining, chain-of-thought, and ReAct — with business examples and best practices.

- **[3.3 Grounding, RAG, and Sampling Parameters](./3.3_grounding_and_rag.md)**: A thorough treatment of grounding types (first-party data, third-party data, Google Search), how RAG works step by step, Google Cloud's grounding offerings, and a complete guide to sampling parameters including temperature, Top-P, token limits, and safety settings.