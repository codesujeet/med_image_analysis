import streamlit as st
from pathlib import Path
import google.generativeai as genai


google_api_key = st.secrets["GOOGLE_API_KEY"]

# Configure Generative AI Model
genai.configure(api_key=google_api_key)

# Generation config and safety settings remain the same
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompts = [
    """
    You are a domain expert in medical image analysis. You are tasked with 
    examining medical images for a renowned hospital.
    Your expertise will help in identifying or 
    discovering any anomalies, diseases, conditions or
    any health issues that might be present in the image.
    
    Your key responsibilites:
    1. Detailed Analysis : Scrutinize and thoroughly examine each image, 
    focusing on finding any abnormalities.
    2. Analysis Report : Document all the findings and 
    clearly articulate them in a structured format.
    3. Recommendations : Basis the analysis, suggest remedies, 
    tests or treatments as applicable.
    4. Treatments : If applicable, lay out detailed treatments 
    which can help in faster recovery.
    
    Important Notes to remember:
    1. Scope of response : Only respond if the image pertains to 
    human health issues.
    2. Clarity of image : In case the image is unclear, 
    note that certain aspects are 
    'Unable to be correctly determined based on the uploaded image'
    3. Disclaimer : Accompany your analysis with the disclaimer: 
    "Consult with a Doctor before making any decisions."
    4. Your insights are invaluable in guiding clinical decisions. 
    Please proceed with the analysis, adhering to the 
    structured approach outlined above.
    
    Please provide the final response with these 5 headings : 
    Detailed Analysis, Analysis Report, Recommendations and Treatments
    and add conclusions at the end.
    """
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                            generation_config=generation_config,
                            safety_settings=safety_settings)

# Page Configuration
st.set_page_config(page_title="Visual Medical Assistant", page_icon="🩺", layout="wide")

# Sidebar
with st.sidebar:
    st.title("About the App 📋")
    st.markdown("""
    ### Welcome to Visual Medical Assistant! 🏥
    
    This application leverages advanced AI technology to assist in medical image analysis. 
    It's designed to help healthcare professionals and individuals get preliminary insights 
    from medical images.
    
    #### Key Features 🌟
    - Upload and analyze medical images
    - Get detailed analysis reports
    - Receive potential treatment recommendations
    - Quick and easy to use interface
    
    #### How to Use 📝
    1. Upload your medical image using the file uploader
    2. Click on "Generate Analysis"
    3. Review the detailed analysis provided
    
    #### Important Note ⚠️
    This tool is meant for assistance purposes only and should not replace 
    professional medical advice. Always consult with qualified healthcare 
    professionals for proper diagnosis and treatment.
    
    #### Supported Image Types 🖼️
    - PNG
    - JPG/JPEG
    """)
    
    st.markdown("---")
    st.markdown("### Developer Info 👨‍💻")
    st.markdown("""
    Built with:
    - Streamlit
    - Google's Gemini Pro Vision
    - Python
    """)

# Main Content
st.title("Visual Medical Assistant 🏥")
st.subheader("An app to help with medical analysis using images")

# Create columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    file_uploaded = st.file_uploader('Upload the image for Analysis', 
                                   type=['png','jpg','jpeg'])

with col2:
    if file_uploaded:
        st.image(file_uploaded, width=200, caption='Uploaded Image')

submit = st.button("Generate Analysis", type="primary")

if submit:
    if file_uploaded:
        with st.spinner('Analyzing image... Please wait...'):
            image_data = file_uploaded.getvalue()
            image_parts = [
                {
                    "mime_type": "image/jpg",
                    "data": image_data
                }
            ]
            prompt_parts = [
                image_parts[0],
                system_prompts[0],
            ]
            response = model.generate_content(prompt_parts)
            
            if response:
                st.success('Analysis Complete!')
                st.title('Detailed analysis based on the uploaded image')
                st.write(response.text)
    else:
        st.error('Please upload an image first!')
