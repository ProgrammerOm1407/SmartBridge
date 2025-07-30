# Blog Generator using LLaMA 2 and Streamlit

**Developed by Om Chavan**  
*Created as a university project.*

This project generates customized blog content using the LLaMA 2 language model. Built with Streamlit, it allows users to specify the topic, audience, and word count to get high-quality blog posts.

## Setup

### Prerequisites
- Python 3.8 or higher
- At least 4GB of free disk space (for the model file)
- 8GB+ RAM recommended for smooth operation

### Installation Steps

1. **Clone or download this repository**
```bash
git clone <repository-url>
cd SmartBridge-master
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download the LLaMA 2 model**
   - Visit: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML  
   - Download: `llama-2-7b-chat.ggmlv3.q4_0.bin` (approximately 3.8 GB)
   - Place it inside the `models/` folder
   - Final path should be: `models/llama-2-7b-chat.ggmlv3.q4_0.bin`

   **Important:** The model file is too large to be hosted on GitHub. You must manually download it from the link above.

5. **Run the application**
```bash
streamlit run app.py
```
or
```bash
python -m streamlit run app.py
```

6. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to that URL manually

## Troubleshooting

### Common Issues:
- **"Model file not found"**: Ensure the model file is in the correct location (`models/llama-2-7b-chat.ggmlv3.q4_0.bin`)
- **Out of memory errors**: Try using a smaller word count or restart the application
- **Slow generation**: This is normal for large language models; generation can take 1-5 minutes depending on your hardware

### System Requirements:
- **Minimum**: 4GB RAM, 4GB free disk space
- **Recommended**: 8GB+ RAM, SSD storage for better performance
