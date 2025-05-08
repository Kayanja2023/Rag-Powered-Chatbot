# Evaluation: Validating Project Requirements with Chatbot Prompts

This document evaluates the Clickatell Q&A chatbot’s performance against the key project requirements. Each prompt demonstrates how the chatbot meets expectations in terms of knowledge retrieval, brand tone, structured formatting, fallback logic, and technical clarity.

---

## Requirement 1: Accurate Retrieval from Knowledge Base

**Query:** What is Clickatell's mission?

**Bot Response:**
> Clickatell's mission is to make commerce in chat accessible to everyone, everywhere.

**Validation:**
- Correct factual match with embedded knowledge
- Concise and brand-aligned tone
- Demonstrates successful document retrieval

---

## Requirement 2: Structured Response Using Templating

**Query:** What services are included in the Chat Commerce Platform?

**Bot Response:**
> - Multi-channel messaging
> - In-chat payments
> - Live support across communication platforms

**Validation:**
- Uses bullet-point structure per prompt template
- Pulls accurate data from vector store
- Clear, concise language aligned with tone guidelines

---

## Requirement 3: Developer-Focused Information Delivery

**Query:** How do I authenticate API requests?

**Bot Response:**
> Include your API Key in the Authorization header and use HTTPS with TLS 1.2 or higher.

**Validation:**
- Technical accuracy from developer documentation
- Plain, actionable second-person phrasing
- Response follows prompt formatting guidance

---

## Requirement 4: In-Scope Company Information

**Query:** Who is the CEO of Clickatell?

**Bot Response:**
> Pieter de Villiers is the CEO of Clickatell.

**Validation:**
- Confirms company-specific info retrieval
- Uses direct, clear phrasing
- Pulled directly from knowledge base

---

## Requirement 5: Fallback Triggering on Nonsensical Input

**Query:** Can you enable quantum features on my account?

**Bot Response:**
> I'm not confident I can assist with that. Let me connect you to a live agent.

**Validation:**
- No hallucination or incorrect answer
- Triggers fallback message exactly as specified
- Reflects instruction to never guess

---

## Requirement 6: Product Tier Explanation

**Query:** What does the Interact plan include?

**Bot Response:**
> The Interact plan includes:
> - Chat Flow
> - Chat Desk
> - CRM integration

**Validation:**
- Structured in clear bullet points
- Retrieves correct tier features
- Matches product documentation language

---

## Requirement 7: Workflow Instruction for Developers

**Query:** How do I send a test SMS?

**Bot Response:**
> 1. Make a POST request to the One API
> 2. Include the message and destination number
> 3. Monitor the callback URL for delivery status

**Validation:**
- Accurate, ordered steps
- Response tailored to developer use case
- Matches example format from system prompt

---