import google.generativeai as genai
from PIL import Image
import streamlit as st
import tempfile

# Replace with your actual API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("Gemini Image Description App")

uploaded_file = st.camera_input("Take a picture")

if uploaded_file is not None:
    try:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(bytes_data)
            image = Image.open(temp_file.name)

        st.image(image, caption="Captured Image", use_container_width=True)

        system_prompt = ("당신은 10년 이상 분리수거를 해온 분리수거의 달인 입니다.\n", "한국의 분리수거 방식을 정확하게 인지하고 가이드를 해주세요.")
        user_prompt = st.text_input("사진에 대해 묻고싶은 내용을 입력해주세요:", "어떻게 버려야하나요?")

        if st.button("답변 생성"):
            try:
                model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=system_prompt)  # Or "gemini-pro-vision"
                st.write("Generated Description:")

                # Define a generator function to stream responses
                def generate_stream_chunks():
                    response_iterable = model.generate_content(
                        [user_prompt, image],
                        stream=True
                    )
                    for chunk in response_iterable:
                        if hasattr(chunk, 'text') and chunk.text:
                            yield chunk.text

                st.write_stream(generate_stream_chunks)
            except Exception as e:
                st.error(f"Error during text generation: {e}")
    except Exception as e:
        st.error(f"Error processing image: {e}")
