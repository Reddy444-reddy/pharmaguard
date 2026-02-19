import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def generate_explanation(context, mode="clinician"):
    """
    Generate clinical explanation for pharmacogenomic finding.
    
    Safety: LLM only generates explanation text.
    Risk decision is made deterministically by rule engine.
    
    Args:
        context (dict): Structured clinical context
        mode (str): "clinician" or "patient"
    
    Returns:
        dict: {"summary": str, "mechanism": str}
    """
    
    if mode == "clinician":
        prompt = f"""You are a pharmacogenomics clinical decision support assistant.

Context:
- Gene: {context['gene']}
- Diplotype: {context['diplotype']}
- Phenotype: {context['phenotype']}
- Drug: {context['drug']}
- Risk Label: {context['risk_label']}
- Severity: {context['severity']}
- Recommendation: {context['recommendation']}

Task: Explain the pharmacokinetic mechanism and justify this recommendation.

Format your response as:
1. Mechanism: [Explain how the gene metabolizes this drug]
2. Clinical Implication: [Why this phenotype affects this drug]
3. Guideline Alignment: [Why this recommendation is appropriate]

CRITICAL: Do NOT change or question the risk decision. You are explaining, not deciding."""

    elif mode == "patient":
        prompt = f"""Explain in simple, clear language (no jargon):

The patient's genetic test shows: {context['gene']} {context['diplotype']}
This means they are a: {context['phenotype']}
They are prescribed: {context['drug']}
The system assessment: {context['risk_label']}

Explain:
- What their genetic result means
- Why this drug may not work well for them
- What safe alternatives exist

Keep it simple. Use everyday language."""

    else:
        raise ValueError(f"Invalid mode: {mode}. Use 'clinician' or 'patient'.")
    
    # Check if OpenAI API key is set
    if not OPENAI_AVAILABLE or not os.getenv("OPENAI_API_KEY"):
        # Fallback: return template-based explanation
        return _fallback_explanation(context, mode)
    
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300
        )
        
        text = response["choices"][0]["message"]["content"]
        
        return {
            "summary": text,
            "mechanism": text
        }
    
    except Exception as e:
        # Fallback if API fails
        return _fallback_explanation(context, mode)


def _fallback_explanation(context, mode):
    """
    Fallback explanation template when LLM is unavailable.
    Ensures system still works without API.
    """
    
    if mode == "clinician":
        explanation = f"""Pharmacokinetic Analysis:

Gene: {context['gene']}
Diplotype: {context['diplotype']}
Phenotype: {context['phenotype']}

Drug: {context['drug']}
Risk Classification: {context['risk_label']}
Severity: {context['severity']}

Mechanism:
The {context['gene']} {context['phenotype']} status indicates reduced metabolic capacity for {context['drug']}.

Clinical Implication:
{context['drug']} bioavailability and therapeutic efficacy will be compromised.

Guideline Alignment:
This recommendation aligns with Clinical Pharmacogenetics Implementation Consortium (CPIC) guidance.

Recommended Action:
{context['recommendation']}"""
    
    else:  # patient mode
        explanation = f"""Your Personalized Drug Information:

Your genetic profile: {context['gene']} {context['diplotype']}
This means you are a {context['phenotype']} for this gene group.

About {context['drug']}:
Based on your genetics, {context['drug']} may not work as well for you.

Assessment Level: {context['risk_label']}

What You Should Do:
{context['recommendation']}

Always discuss this with your healthcare provider."""
    
    return {
        "summary": explanation,
        "mechanism": explanation
    }
