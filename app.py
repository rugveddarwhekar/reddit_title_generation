import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access API key from environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Set up Gemini API
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1, api_key=gemini_api_key)

# Load past titles and descriptions
past_data = [
    {"build_id": "AP31.240617.009", "version_name": "Android 15 Beta 4", "title": "[5 min survey] Tells us what you think about Android 15 Beta 4", "description": "Hi Beta users, Thank you for your continued support. Please share your latest experience on Android 15 Beta 4 by filling out our 5 minute anonymous survey. This survey is only for devices running Beta 4 (AP31.240617.009). You can verify this by going to Settings > About Phone/Tablet. We look forward to your feedback!"},
    {"build_id": "AP31.240322.018", "version_name": "Android 15 Beta 1", "title": "[5 min survey] Tells us what you think about Android 15 Beta 1", "description": "Hi Beta users, Thank you for your continued support. Please share your latest experience on Android 15 Beta 1 by filling out our 5 minute anonymous survey. This survey is only for devices running Beta 1 (AP31.240322.018). You can verify this by going to Settings > About Phone/Tablet. We look forward to your feedback!"},
    {"build_id": "AP31.240617.015", "version_name": "Android 15 Beta 4.2", "title": "[5 min survey] Tells us what you think about Android 15 Beta 4.2", "description": "Hi Beta users, Thank you for your continued support. Please share your latest experience on Android 15 Beta 4.2 by filling out our 5 minute anonymous survey. This survey is only for devices running Beta 4 (AP31.240617.015). You can verify this by going to Settings > About Phone/Tablet. We look forward to your feedback!"},
    {"build_id": "AP21.240216.010", "version_name": "Android 14 QPR3 Beta 2", "title": "[5 min survey] Tells us what you think about Android 14 QPR3 Beta 2", "description": "Hi Beta users, Thank you for your continued support. Please share your latest experience on Android 14 QPR3 Beta 2 by filling out our 5 minute anonymous survey. This survey is only for devices running Beta 2 (AP21.240216.010). You can verify this by going to Settings > About Phone/Tablet. We look forward to your feedback!"},
    {"build_id": "AP31.240617.010", "version_name": "Android 15 Beta 3", "title": "[5 min survey] Tells us what you think about Android 15 Beta 3", "description": "Hi Beta users, Thank you for your continued support. Please share your latest experience on Android 15 Beta 3 by filling out our 5 minute anonymous survey. This survey is only for devices running Beta 3 (AP31.240617.010). You can verify this by going to Settings > About Phone/Tablet. We look forward to your feedback!"},
]

# Create a prompt template
prompt_template = PromptTemplate(
    input_variables=["build_id", "version_name", "past_data"],
    template="""
    Given the following information:

    Build ID: {build_id}
    Version Name: {version_name}

    And considering these past titles and descriptions:

    {past_data}

    Generate a new title and description for a post about this build and version. Follow the same format of the past data.
    """
)

# Set up LangChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Streamlit App
st.title("Post Title & Description Generator")

# Take new build ID and version name as input
new_build_id = st.text_input("New Build ID")
new_version_name = st.text_input("New Version Name")

if st.button("Generate"):
    if new_build_id and new_version_name:
        # Format past data for the prompt
        formatted_past_data = "\n".join([f"- {item['title']}: {item['description']}" for item in past_data])

        # Use the new build ID and version name in the prompt
        response = chain.run(
            {
                "build_id": new_build_id,
                "version_name": new_version_name,
                "past_data": formatted_past_data
            }
        )

        st.write(response)

    else:
        st.warning("Please enter both New Build ID and New Version Name.")
