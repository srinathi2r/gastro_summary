import streamlit as st
import openai
import os

# Initialize OpenAI client with your API key
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found in environment variables")
else:
    openai.api_key = api_key

def generate_summary(histo_date, colonoscopy_date, detailed_finding_histo, detailed_finding_colonoscopy):
    # Define the prompt
    prompt = f"""
    Detailed Findings - Histo: {detailed_finding_histo}
    Detailed Findings - Colonoscopy: {detailed_finding_colonoscopy}

    This patient underwent colonoscopy on {colonoscopy_date} with a total of (number) adenomas. There were (number) polyps with villous histology and (number) polyps with high-grade dysplasia. The largest adenoma was (number)mm in size. In addition, (number) sessile serrated lesions were detected and the largest was (number)mm in size. Based on the USMTF polyp surveillance recommendations, the patient requires a repeat colonoscopy in (number) years.

    Provide the structured summary by filling in the numbers:
    """

    # Call OpenAI API
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
        )

    # Extract the response
    summary = response.choices[0].text.strip()
    return summary

def main():
    st.title("Gastro Summary Tool")

    # Input fields
    histo_date = st.text_input("Histo Date")
    colonoscopy_date = st.text_input("Colonoscopy Date")
    detailed_finding_histo = st.text_area("Detailed Findings - Histo")
    detailed_finding_colonoscopy = st.text_area("Detailed Findings - Colonoscopy")

    if st.button("Generate Summary"):
        if not api_key:
            st.error("OpenAI API key not found. Please set the API key in environment variables.")
        else:
            summary = generate_summary(histo_date, colonoscopy_date, detailed_finding_histo, detailed_finding_colonoscopy)
            st.subheader("Generated Summary")
            st.write(summary)

if __name__ == "__main__":
    main()
