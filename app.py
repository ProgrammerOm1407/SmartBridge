import streamlit as st
from ctransformers import AutoModelForCausalLM

# Load LLaMA 2 model
@st.cache_resource
def load_model(thread_count=4):
    import os
    model_path = "models/llama-2-7b-chat.ggmlv3.q4_0.bin"
    
    if not os.path.exists(model_path):
        st.error(f"❌ Model file not found at {model_path}")
        st.error("Please download the model file from: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML")
        st.error("And place it in the 'models/' folder as instructed in the README.")
        st.stop()
    
    try:
        return AutoModelForCausalLM.from_pretrained(
            model_path,
            model_type="llama",
            # Optimization parameters for faster inference
            gpu_layers=0,  # Use CPU (set to higher number if you have GPU)
            threads=thread_count,  # Dynamic thread count
            context_length=1024,   # Reduced context for faster processing
            batch_size=1,
        )
    except Exception as e:
        st.error(f"❌ Failed to load model: {str(e)}")
        st.stop()

# Initialize model with default settings
if 'model' not in st.session_state:
    st.session_state.model = load_model()

# App UI
st.title("📝 LLaMA 2 Blog Generator")
st.markdown("<span style='font-size:1.5em; color:#d6336c; font-weight:bold;'>Developed by Om Chavan</span>", unsafe_allow_html=True)
st.markdown("*Created as a university project.*")
st.markdown("Generate high-quality blogs based on topic, audience, and word count.")

# Add some helpful information
with st.expander("ℹ️ How to use this app"):
    st.markdown("""
    1. **Enter a Blog Topic**: Provide a clear and specific topic for your blog post
    2. **Choose Target Audience**: Select who you're writing for (affects tone and complexity)
    3. **Select Length**: Choose how long you want your blog post to be
    4. **Generate**: Click the button and wait for the AI to create your blog
    5. **Download**: Save your generated blog as a text file
    
    **Tips for better results:**
    - Be specific with your topic (e.g., "Benefits of Machine Learning in Healthcare" vs "AI")
    - Consider your audience when choosing complexity level
    - Use Fast Mode for quicker results (slightly lower quality)
    - Shorter blogs generate much faster
    
    **Performance Tips:**
    - Enable Fast Mode for 3-5x faster generation
    - Use 300 words or less for best speed
    - Increase CPU threads if you have a multi-core processor
    - Close other heavy applications while generating
    """)

# Input fields with better descriptions
topic = st.text_input(
    "Enter Blog Topic", 
    placeholder="e.g., 'The Future of Artificial Intelligence in Education'",
    help="Be specific and clear about what you want to write about"
)

audience = st.selectbox(
    "Choose Target Audience", 
    ["Researchers", "Common People", "Data Scientists"],
    help="This affects the tone and complexity of the generated content"
)

length = st.slider(
    "Select Length (in words)", 
    min_value=100, 
    max_value=1000, 
    value=300,
    step=50,
    help="Approximate word count for your blog post"
)

# Performance settings
with st.expander("⚡ Performance Settings (Advanced)"):
    col1, col2 = st.columns(2)
    with col1:
        use_fast_mode = st.checkbox("🚀 Fast Mode", value=True, help="Reduces quality slightly but generates much faster")
        threads = st.slider("CPU Threads", 1, 8, 4, help="More threads = faster generation (if you have multiple CPU cores)")
    with col2:
        max_length = st.slider("Max Output Length", 200, 800, min(length + 100, 500), help="Lower = faster generation")

# Show current settings
if topic:
    estimated_time = "30-60 seconds" if use_fast_mode else "2-5 minutes"
    st.info(f"📝 **Topic**: {topic} | 👥 **Audience**: {audience} | 📏 **Length**: ~{length} words | ⏱️ **Est. Time**: {estimated_time}")

if st.button("Generate Blog"):
    # Input validation
    if not topic or topic.strip() == "":
        st.error("❌ Please enter a blog topic!")
        st.stop()
    
    if len(topic.strip()) < 3:
        st.error("❌ Blog topic should be at least 3 characters long!")
        st.stop()
    
    # Dynamic spinner message based on mode
    spinner_msg = "🚀 Fast generating..." if use_fast_mode else "⏳ Generating blog (high quality)..."
    
    with st.spinner(spinner_msg):
        import time
        start_time = time.time()
        try:
            # Create optimized prompt based on mode
            if use_fast_mode:
                prompt = f"Write a {length}-word blog about '{topic.strip()}' for {audience.lower()}:\n\n"
            else:
                prompt = f"""Write a comprehensive {length}-word blog post about "{topic.strip()}" for {audience.lower()}.
Include introduction, main content, and conclusion.

Blog Post:"""
            
            # Dynamic generation parameters based on fast mode
            if use_fast_mode:
                result = st.session_state.model(
                    prompt, 
                    max_new_tokens=min(max_length, 300),  # Shorter for speed
                    temperature=0.9,      # Higher for faster sampling
                    top_p=0.8,           # More focused sampling
                    top_k=30,            # Smaller vocabulary
                    repetition_penalty=1.15,
                    stop=["</s>", "\n\n\n", "---"]
                )
            else:
                result = st.session_state.model(
                    prompt, 
                    max_new_tokens=max_length,
                    temperature=0.7,      # Lower for better quality
                    top_p=0.95,          # More diverse sampling
                    top_k=50,            # Larger vocabulary
                    repetition_penalty=1.1,
                    stop=["</s>", "\n\n---", "END"]
                )
            
            if not result or len(result.strip()) < 50:
                st.error("❌ Generated content is too short. Please try again with a different topic.")
                st.stop()
            
            # Calculate generation time
            generation_time = time.time() - start_time
            
            st.success(f"✅ Blog generated successfully in {generation_time:.1f} seconds!")
            
            # Show performance stats
            word_count = len(result.split())
            st.info(f"📊 **Stats**: {word_count} words generated | ⏱️ {generation_time:.1f}s | 🚀 Mode: {'Fast' if use_fast_mode else 'Quality'}")
            
            st.markdown("### Generated Blog:")
            st.markdown(result)
            
            # Download button with better filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"blog_{topic.replace(' ', '_')}_{timestamp}.txt"
            st.download_button(
                "📥 Download Blog", 
                result, 
                file_name=filename,
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"❌ Error generating blog: {str(e)}")
            st.error("Please try again with a different topic or check your model setup.")
