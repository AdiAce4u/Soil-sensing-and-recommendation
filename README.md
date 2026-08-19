
#  Ecocatalysts: Soil Sensing and Recommendation Intelligence System

Welcome to **Ecocatalysts**, an AI-powered smart soil monitoring and recommendation system! This application is designed to help farmers, agricultural experts, and hobbyists evaluate soil quality, detect anomalies in sensor data, generate actionable recommendations using a Large Language Model (LLM), and identify plant diseases from leaf images.

 **Live Demo:** [Check out the Gradio app on Hugging Face Spaces](https://huggingface.co/spaces/sleepy-panda21/Ecocatalysts)

---

##  Key Features &  Models Used

This project relies on a multi-model architecture to process different types of agricultural data. Here is a detailed breakdown of the algorithms and pre-trained models implemented:

### 1.  Soil Data Anomaly Detection (`iso_model.pkl`)
- **Purpose:** To detect complex, multivariate statistical anomalies within soil data that simple threshold checks might miss.
- **Model:** **Isolation Forest** (implemented via `scikit-learn`).
- **Data Preprocessing:** Inputs (Nitrogen, Phosphorus, Potassium, pH, and Temperature) are transformed using a fitted **Standard Scaler** (`scaler.pkl`) before being passed into the model.
- **Rule-based Evaluation:** The ML model is supplemented by static threshold rules to generate human-readable warnings (e.g., highlighting highly acidic soil [pH < 5.5], low nitrogen levels [< 240], or dangerous temperatures).

### 2.  LLM-Based Soil Health Recommendations (`soil_llm.py`)
- **Purpose:** To act as an AI agronomist, providing customized, actionable advice to improve crop yield and soil health based on the current readings.
- **Pre-trained Model:** **`TinyLlama/TinyLlama-1.1B-chat-v1.0`**
- **Implementation:** The model is fetched via Hugging Face `transformers` and runs inference locally on the CPU using PyTorch (`torch`).
- **Prompt Engineering:** The system concatenates the 7 core soil parameters (including Moisture and EC) along with the detected anomalies into a context-aware prompt, asking the TinyLlama model to generate detailed recommendations.

### 3.  Plant Disease Image Analysis (`plant_disease_model.keras`)
- **Purpose:** A computer vision module designed to analyze plant leaves and predict diseases instantly.
- **Model Architecture:** A deep learning vision model built and serialized using **TensorFlow / Keras**.
- **Data Pipeline:** 
  - User-uploaded images are processed using `Pillow` (PIL).
  - Images are resized to **224x224 pixels**.
  - Pixel values are normalized (`/ 255.0`) and expanded into tensors for inference.
- **Classification:** The model maps predictions to **38 distinct classes** (defined in `labels.py`). It is capable of identifying healthy leaves alongside specific diseases like:
  - *Apple Scab*
  - *Potato Late Blight*
  - *Tomato Mosaic Virus*
  - *Corn Northern Leaf Blight*, and many more.

---

## 🛠️ Technology Stack

*   **Frontend UI:** [Gradio](https://gradio.app/) with custom CSS for an interactive and responsive user experience.
*   **Machine Learning (Tabular Data):** Scikit-Learn, Pandas, NumPy, and Joblib.
*   **Computer Vision:** TensorFlow (v2.17.0), Keras, and Pillow.
*   **Natural Language Processing:** Hugging Face Transformers and PyTorch.
*   **Data Science & Exploration:** Jupyter Notebooks, Matplotlib, and Seaborn.

---

## Project Structure

- `app.py`: The main Gradio application script that renders the UI and integrates the anomaly, CV, and LLM models.
- `soil_llm.py`: Handles the local execution of the TinyLlama LLM and cleans the generated output.
- `labels.py`: Contains a Python array mapping the 38 plant disease classes to the vision model's output indices.
- `iso_model.pkl` & `scaler.pkl`: Serialized Scikit-Learn models for the anomaly detection feature.
- `plant_disease_model.keras`: Serialized TensorFlow deep learning model for image classification.
- `Disease_detection.ipynb` & `anamoly_detection.ipynb`: The Jupyter notebooks originally used to train and export these custom models.
- `requirements.txt`: Contains all project dependencies to reproduce the environment.

---

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Soil-sensing-and-recommendation
   ```

2. **Install the dependencies:**
   It is recommended to use a Python virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```
   The application will start a local Gradio server and provide a URL (typically `http://127.0.0.1:7860/`) where you can interact with the app in your browser.

---
*Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference*
