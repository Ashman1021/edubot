"""Sidebar components for EduBot."""

import streamlit as st
from typing import List, Any
from processors.document_processor import DocumentProcessor
from processors.image_processor import ImageProcessor
from PIL import Image

def setup_sidebar() -> None:
    """Setup the simplified sidebar for media uploads only."""
    with st.sidebar:
        st.header("📁 Upload Files")
        
        # Document upload section
        _setup_document_upload()
        
        # Image upload section
        _setup_image_upload()
        
        # Display uploaded content
        _display_uploaded_content()
        
        # Clear files button
        _setup_clear_button()

def _setup_document_upload() -> None:
    """Setup document upload section."""
    st.subheader("📄 Documents")
    
    if not DocumentProcessor.is_supported():
        st.warning("⚠️ Install: pip install PyPDF2 python-docx pandas openpyxl")
    
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=['pdf', 'docx', 'xlsx', 'xls', 'csv'],
        accept_multiple_files=True,
        help="Upload PDF, DOCX, Excel, or CSV files"
    )
    
    if uploaded_files:
        process_uploaded_files(uploaded_files)

def _setup_image_upload() -> None:
    """Setup image upload section."""
    st.subheader("🖼️ Images")
    
    if not ImageProcessor.is_supported():
        st.warning("⚠️ Install: pip install Pillow")
    
    uploaded_images = st.file_uploader(
        "Upload images",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
        accept_multiple_files=True,
        help="Upload images for analysis"
    )
    
    if uploaded_images:
        process_uploaded_images(uploaded_images)

def _display_uploaded_content() -> None:
    """Display uploaded content summary."""
    if st.session_state.uploaded_documents:
        st.write("**📄 Documents:**")
        for doc in st.session_state.uploaded_documents:
            st.write(f"📄 {doc['name']}")
    
    if st.session_state.uploaded_images:
        st.write("**🖼️ Images:**")
        for img in st.session_state.uploaded_images:
            st.write(f"🖼️ {img['name']}")

def _setup_clear_button() -> None:
    """Setup clear files button."""
    if (st.session_state.uploaded_documents or st.session_state.uploaded_images):
        if st.button("🗑️ Clear All Files"):
            st.session_state.uploaded_documents = []
            st.session_state.uploaded_images = []
            st.rerun()

def process_uploaded_files(uploaded_files: List[Any]) -> None:
    """Process uploaded files and extract content."""
    processor = DocumentProcessor()
    
    for uploaded_file in uploaded_files:
        if any(doc['name'] == uploaded_file.name for doc in st.session_state.uploaded_documents):
            continue
        
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        try:
            content = processor.process_file(uploaded_file, file_type)
            
            st.session_state.uploaded_documents.append({
                'name': uploaded_file.name,
                'type': file_type,
                'content': content,
                'size': getattr(uploaded_file, 'size', 0)
            })
            
            st.success(f"✅ Processed: {uploaded_file.name}")
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")

def process_uploaded_images(uploaded_images: List[Any]) -> None:
    """Process uploaded images."""
    processor = ImageProcessor()
    
    for uploaded_image in uploaded_images:
        if any(img['name'] == uploaded_image.name for img in st.session_state.uploaded_images):
            continue
        
        try:
            result = processor.process_image(uploaded_image)
            
            if result['success']:
                st.session_state.uploaded_images.append({
                    'name': uploaded_image.name,
                    'base64_data': result['base64_data'],
                    'original_size': result['original_size'],
                    'processed_size': result['processed_size'],
                    'file_size': result['file_size'],
                    'format': result['format']
                })
                
                st.success(f"✅ Processed: {uploaded_image.name}")
                
                image = Image.open(uploaded_image)
                st.image(image, caption=uploaded_image.name, width=200)
                
            else:
                st.error(f"❌ Error processing {uploaded_image.name}: {result['error']}")
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_image.name}: {str(e)}")