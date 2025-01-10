import streamlit as st
import requests
import json
import re

st.write("""
         # Demo
        *get data from image*
         """)

uploaded_images = st.file_uploader("Tải một hoặc nhiều ảnh", type=[
                 'jpg', 'png', 'jpeg'], accept_multiple_files=True, label_visibility="visible")
uploaded_pdf = st.file_uploader("Tải một file pdf", type=[
                 'pdf'], label_visibility="visible")
submit_btn = st.button("Submit")
            
images_api_url = "http://127.0.0.1:5000/api/image"
pdf_api_url = "http://127.0.0.1:5000/api/pdf"
if submit_btn:
    if uploaded_images:
        images = []
        for img in uploaded_images:
            # Convert the image to bytes
            img_bytes = img.read()
            # img_pil = Image.open(BytesIO(img_bytes))
            name_img = img.name
            type_img = img.type
            images.append(('images', (name_img, img_bytes, type_img)))
        # Display images in a single row
        cols = st.columns(len(uploaded_images))
        for i, img in enumerate(uploaded_images):
            with cols[i]:
              st.image(img, caption="Uploaded Image", use_column_width=True, width=25)
        # Send the POST request`
        response = requests.post(images_api_url, files=images)

        # Check the response
        if response.status_code == 200:
            st.success("Image uploaded successfully")
            data = response.json()
            contents = data.get("contents")
            # Tìm đoạn JSON trong markdown
            
            match = re.search(r'```json\n(.*?)\n```', contents, re.DOTALL)
            if match:
                json_string = match.group(1)  # Lấy phần JSON bên trong
                json_object = json.loads(json_string)  # Chuyển thành JSON object
                st.json(json_object)
            else:
                st.warning("No JSON found in the response")
        else:
            st.error("Failed requests to server")
    elif uploaded_pdf:
        pdf_file = uploaded_pdf.read()
        pdf_name = uploaded_pdf.name
        pdf_type = uploaded_pdf.type
        files = {'file': (pdf_name, pdf_file, pdf_type)}

        response = requests.post(pdf_api_url, files=files)

        if response.status_code == 200:
            st.success("PDF uploaded successfully")
            data = response.json()
            contents = data.get("contents")
            
            match = re.search(r'```json\n(.*?)\n```', contents, re.DOTALL)
            if match:
                json_string = match.group(1)
                json_object = json.loads(json_string)
                st.json(json_object)
            else:
                st.warning("No JSON found in the response")
        else:
            st.error("Failed requests to server")
    else:
        st.warning("Please upload an Image or PDF file")
        
    
                
st.text_input("Tên thuốc")
st.text_input("Dạng bào chế")
st.text_input("Thành phần")
st.text_input("Cách đóng gói")
st.text_input("Chỉ định")
st.text_input("chống chỉ định")
st.text_input("Cách dùng")
st.text_input("Ngày sản xuất")
st.text_input("Hạn sử dụng")
st.text_input("Điều kiện bảo quản")
st.text_input("Khuyến cáo")
st.text_input("Tên cơ sở sản xuất thuốc")
st.text_input("Địa chỉ cơ sở sản xuất thuốc")
st.text_input("Xuất xứ của thuốc")

