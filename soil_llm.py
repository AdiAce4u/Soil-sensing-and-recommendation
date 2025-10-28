from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "TinyLlama/TinyLlama-1.1B-chat-v1.0"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

#open source model

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.float32,  
    device_map=None             
).to("cpu")



def clean_output(raw_output):
    
    if "Provide detailed, actionable recommendations" in raw_output:
        cleaned = raw_output.split("Provide detailed, actionable recommendations")[1]
    else:
        cleaned = raw_output

    
    cleaned = cleaned.replace("</s>", "").strip()
    return cleaned


def get_soil_recommendation(N, P, K, pH, Temp, Moisture, EC, explanation):
    soil_data = {
        "Nitrogen (mg/kg)": N,
        "Phosphorus (mg/kg)": P,
        "Potassium (mg/kg)": K,
        "pH": pH,
        "Temperature (°C)": Temp,
        "Moisture (%)": Moisture,
        "EC (dS/m)": EC
    }

    prompt = f"""
You are a soil expert. Given the following soil data:

{soil_data}

Analysis of anomalies:
{explanation}

Provide detailed, actionable recommendations for improving soil health and crop growth.
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=250,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )
    
    raw_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    recommendation = clean_output(raw_output)

    return recommendation
