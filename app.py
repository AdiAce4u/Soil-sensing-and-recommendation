
#CSS File
css = """
.title {
    text-align: center;
    color: #2e7d32;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 16px;
    font-weight: 400;
    margin-top: 0;
    margin-bottom: 20px;
}

.header-box {
    background: linear-gradient(90deg, #4CAF50, #81C784);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.snsdt{
    background-color: ;
    border-radius: 10px;
    padding: 7px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    width: 100%;
    
    
}

.input-row {
    display: flex;
    gap: 10px; 
    margin-bottom: 10px;
}


.npk-input {
    flex: 1; 
}


.gr-button {
    background-color: #2e7d32;
    color: white;
    font-weight: 600;
    flex: 1;
}

.gr-button:hover {
    background-color: #1b5e20;
}

.gr-textbox, .gr-number {
    border-radius: 8px;
    border: 1px solid #ccc;
    padding: 8px;
    width: 100%;
}
"""

import gradio as gr
import joblib
import numpy as np
from soil_llm import get_soil_recommendation


# Load model + scaler
iso = joblib.load("iso_model.pkl")
scaler = joblib.load("scaler.pkl")

# load image prediction model
import tensorflow as tf
from tensorflow.keras.models import load_model
from labels import class_names

model = load_model("plant_disease_model.keras")

# image prediction function

def preprocess_image(img):
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict(img):
    if img is None:
        return "Please upload an image first!"
    processed = preprocess_image(img)
    prediction = model.predict(processed)
    class_id = np.argmax(prediction)
    predicted_class = class_names[class_id]
    confidence = round(float(np.max(prediction)) * 100, 2)
    return f" {predicted_class}\nConfidence: {confidence}%"


# Natural language explanation function
def explain(row , moisture=None , ec=None):
    reasons = []

    # threshold checks
    if row['Nitrogen'] <240 :
        reasons.append("Low quantity of Nitrogen present in soil")
    if row['Nitrogen'] > 480:
        reasons.append("High quantity of Nitrogen present in soil")

    if row['Phosphorus'] <11 :
        reasons.append("Low quantity of Phosphorus present in soil")
    if row['Phosphorus'] > 22:
        reasons.append("High quantity of Phosphorus present in soil")


    if row['Potassium'] < 110:
        reasons.append("Low quantity of Potassium present in soil")
    if row['Potassium'] > 280:
        reasons.append("High quantity of Potassium present in soil")  

    if row['pH_Value'] < 5.5:
        reasons.append("The soil have high acidic content")
    if row['pH_Value'] > 7.5:
        reasons.append("The soil is highly alkaline in nature")

    if row['Temperature'] < 10 or row['Temperature'] > 24:
        reasons.append("Temperature out of recommended range (10-24°C)")
 

    # Anamoly detection
    if row.get('anomaly', 1) == -1 and len(reasons) == 0:
        reasons.append("\n Unusual combination of values detected by model")

    return "\n".join(reasons)


def detect_anomaly(N, P, K, pH, Temp):
    
    data = np.array([[N, P, K, pH, Temp]])
    scaled = scaler.transform(data)

    pred = iso.predict(scaled)[0]
    
    row = {
        'Nitrogen': N,
        'Phosphorus': P,
        'Potassium': K,
        'pH_Value': pH,
        'Temperature': Temp
    }

    status = "Normal Reading " if pred == 1 else "Anomaly Detected  "
    reason = explain(row)

    return f"{status}\n\nReasons:\n{reason}"


def analyze_soil(N, P, K, pH, Temp, Moisture, EC):
    
    row = {'Nitrogen': N, 'Phosphorus': P, 'Potassium': K,
           'pH_Value': pH, 'Temperature': Temp}
    explanation = explain(row, moisture=Moisture, ec=EC)

    # to LLM
    recommendation = get_soil_recommendation(N, P, K, pH, Temp, Moisture, EC, explanation)
    
    return f"--- Analysis ---\n{explanation}\n\n--- Recommendation ---\n{recommendation}"



# Gradio app
with gr.Blocks(css=css, theme=gr.themes.Soft(primary_hue="teal")) as demo:

    # Header 
    gr.HTML("""
    <div class="header-box">
        <div class="title"> Soil Sensing and Recommendation Intelligence System</div>
        <div class="subtitle">Smart soil monitoring and AI-based recommendations</div>
    </div>
    """)


    with gr.Row(equal_height= True):

       # manual soil data card
        with gr.Column(scale=1):
            with gr.Group(elem_classes="snsdt" ):
                gr.Markdown("### Enter Soil Sensor Data")
                
     
                with gr.Row(elem_classes="input-row"):
                    moisture = gr.Number(label="Moisture (%)")
                    temperature = gr.Number(label="Temperature (°C)")

                with gr.Row(elem_classes="input-row"):
                    ph = gr.Number(label="pH Level")
                    ec = gr.Number(label="EC (dS/m)")

                with gr.Row(elem_classes="input-row"):
                    nitrogen = gr.Number(label="N (kg/ha)", elem_classes="npk-input")
                    phosphorus = gr.Number(label="P (kg/ha)", elem_classes="npk-input")
                    potassium = gr.Number(label="K (kg/ha)", elem_classes="npk-input")

                with gr.Row():
                    submit_btn = gr.Button("Check Anamoly")
                    fetch_btn = gr.Button("Get Recommendation")          
                
                
               
        with gr.Column(scale=1):
            with gr.Group(elem_classes="snsdt"):
                gr.Markdown("## Upload Soil Image")
                image_input = gr.Image(label="Upload an image", type="pil")
                img_btn = gr.Button(" Analyze Image")

    with gr.Row(equal_height = True):
        
        with gr.Column(scale=1):
            with gr.Group(elem_classes="snsdt"):
                output = gr.Textbox(label="Predicted Soil Analysis / Image analysis", lines=2)
                
    with gr.Row():
        with gr.Column(scale=1) :
            with gr.Group(elem_classes="snsdt"):
                 reccomend= gr.Textbox(label="Soil Health Advise", lines= 4)
                

    submit_btn.click(
    fn=detect_anomaly,
    inputs=[nitrogen, phosphorus, potassium, ph, temperature],
    outputs=[output],)
    
    fetch_btn.click(
     fn=analyze_soil,
    inputs=[nitrogen, phosphorus, potassium, ph, temperature, moisture, ec],
    outputs=[reccomend]
    
)   
    img_btn.click(
        fn=predict,
        inputs=[image_input],
        outputs= [output]
    )          


                            
                
                
demo.launch()