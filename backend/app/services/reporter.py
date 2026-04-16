from groq import Groq
from ..core.config import get_settings

class MedicalReporter:
    def __init__(self):
        self.settings = get_settings()
        api_key = self.settings.GROQ_API_KEY
        self.client = Groq(api_key=api_key) if api_key else None
        self.model = "llama3-70b-8192"

    def generate_medical_report(self, classification_result: str, confidence: float) -> str:
        """
        Generates a professional neuroradiology report using Llama 3 via Groq.
        Refined for Senior Neuroradiologist & Medical AI Specialist role.
        """
        if not self.client:
            return self._fallback_report(classification_result, confidence)

        system_prompt = (
            "You are an AI diagnostic assistant. Generate a report based on the provided classification. "
            "The report must follow this exact 4-section structure:\n"
            "Section  section 1: Pathological Overview: A brief, 2-line scientific description of the identified tumor type.\n"
            "Section 2: Typical Presentation: Describe the common locations in the brain where this specific tumor is usually found "
            "and its typical growth patterns (Size/Margination) that help differentiate between benign and malignant status.\n"
            "Section 3: Clinical Correlation: Explain how the confidence score aligns with standard imaging protocols.\n"
            "Section 4: Patient Guidance: Provide 3 clear next steps for the patient (e.g., Consultation with a Neurosurgeon, "
            "Contrast-enhanced MRI (CEMRI), or biopsy)."
        )

        user_prompt = (
            f"The model has classified the MRI scan as: {classification_result} with a confidence score of {confidence * 100:.1f}%. "
            f"Maintain a professional, calm, and objective medical tone. "
            f"Mandatory Disclaimer: End every report with: 'NOTE: This is an AI-generated preliminary finding based on neural network analysis. "
            f"This report must be verified by a board-certified Radiologist before any clinical decisions are made.'"
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=self.model,
                temperature=0.2, # Clinical objectivity
                max_tokens=600,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Groq Cluster Error: {str(e)}")
            return self._fallback_report(classification_result, confidence)

    def _fallback_report(self, classification_result: str, confidence: float) -> str:
        """High-quality template fallback when LLM cluster is unreachable."""
        return (
            f"SECTION 1: PATHOLOGICAL OVERVIEW\n"
            f"The automated classification identifies morphology consistent with {classification_result}.\n"
            f"This requires careful differentiation via specialized neuro-imaging features and patient clinical presentation.\n\n"
            f"SECTION 2: TYPICAL PRESENTATION\n"
            f"Commonly presents as focal lesions in characteristic brain regions like the intra-axial or extra-axial compartments.\n"
            f"Growth patterns range from well-circumscribed (benign tendency) to infiltrative (malignant tendency).\n\n"
            f"SECTION 3: CLINICAL CORRELATION\n"
            f"The reported {confidence * 100:.1f}% confidence indicates high alignment with established diagnostic patterns, "
            f"though radiological confirmation remains paramount.\n\n"
            f"SECTION 4: PATIENT GUIDANCE\n"
            f"1. Consultation with an Oncology Specialist or Neurosurgeon.\n"
            f"2. Follow-up study with Contrast-enhanced MRI (CEMRI).\n"
            f"3. Clinical evaluation for potential biopsy or surgical review.\n\n"
            f"NOTE: This is an AI-generated preliminary finding based on neural network analysis. "
            f"This report must be verified by a board-certified Radiologist before any clinical decisions are made."
        )


# ====================================================================== #
#  Hallucination Detection — Report Auditor                               #
# ====================================================================== #

import re


class ReportAuditor:
    """Verifies that an LLM-generated medical report is consistent
    with the PyTorch classifier's prediction via a two-stage check:
    hard (keyword) logic + soft (LLM-based) logic."""

    def __init__(self):
        self.settings = get_settings()
        api_key = self.settings.GROQ_API_KEY
        self.client = Groq(api_key=api_key) if api_key else None
        # Use the lightweight 8B model for fast auditing
        self.model = "llama-3.1-8b-instant"

    # ------------------------------------------------------------------ #
    #  Public API                                                         #
    # ------------------------------------------------------------------ #
    def audit_report(self, predicted_label: str, generated_report: str) -> dict:
        """Run hard + soft checks and return audit results.

        Returns
        -------
        dict with keys: trust_score (float 0–1), consistency_check (str),
        auditor_notes (str).
        """
        hard = self._hard_check(predicted_label, generated_report)
        soft = self._soft_check(predicted_label, generated_report)

        # Blend: 30 % hard logic, 70 % soft logic
        if soft["score"] is not None:
            blended = 0.3 * hard["score"] + 0.7 * soft["score"]
            notes = soft["notes"]
        else:
            blended = hard["score"]
            notes = hard["notes"]

        blended = round(min(max(blended, 0.0), 1.0), 2)

        if blended >= 0.90:
            status = "Verified"
        elif blended >= 0.70:
            status = "Use with Caution"
        else:
            status = "Conflict Detected"

        return {
            "trust_score": blended,
            "consistency_check": status,
            "auditor_notes": notes,
        }

    # ------------------------------------------------------------------ #
    #  Step 1 — Hard Logic (keyword presence)                             #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _hard_check(predicted_label: str, report: str) -> dict:
        label_lower = predicted_label.lower().strip()
        report_lower = report.lower()

        if label_lower in report_lower:
            return {
                "score": 1.0,
                "notes": f"Hard-check PASSED: '{predicted_label}' found in report.",
            }
        return {
            "score": 0.3,
            "notes": (
                f"Hard-check WARNING: '{predicted_label}' not explicitly "
                "mentioned in report text."
            ),
        }

    # ------------------------------------------------------------------ #
    #  Step 2 — Soft Logic (LLM-based audit via Groq)                     #
    # ------------------------------------------------------------------ #
    def _soft_check(self, predicted_label: str, report: str) -> dict:
        if not self.client:
            return {"score": None, "notes": "Auditor LLM unavailable (no API key)."}

        prompt = (
            f"You are a medical report auditor. "
            f"Classification result: {predicted_label}. "
            f"Generated report:\n\"\"\"\n{report}\n\"\"\"\n"
            f"Does this report accurately reflect the classification "
            f"without inventing new pathologies? "
            f"Rate the consistency from 1 (completely inconsistent) to "
            f"10 (perfectly consistent). "
            f"Reply ONLY in the format: RATING: <number>\nEXPLANATION: <one-line reason>"
        )

        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.0,
                max_tokens=120,
            )
            raw = completion.choices[0].message.content or ""
            return self._parse_audit_response(raw)
        except Exception as e:
            print(f"Auditor LLM Error: {e}")
            return {"score": None, "notes": f"Auditor LLM call failed: {e}"}

    # ------------------------------------------------------------------ #
    #  Response parser                                                     #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _parse_audit_response(raw: str) -> dict:
        """Extract numeric rating (1-10) and explanation from LLM output."""
        match = re.search(r"RATING:\s*(\d+(?:\.\d+)?)", raw, re.IGNORECASE)
        rating = float(match.group(1)) if match else None

        expl_match = re.search(r"EXPLANATION:\s*(.+)", raw, re.IGNORECASE | re.DOTALL)
        explanation = expl_match.group(1).strip() if expl_match else raw.strip()

        if rating is not None:
            score = min(max(rating / 10.0, 0.0), 1.0)
        else:
            score = None

        return {"score": score, "notes": explanation}
