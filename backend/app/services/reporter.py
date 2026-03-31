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
