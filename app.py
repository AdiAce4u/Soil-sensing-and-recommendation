import gradio as gr

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

# Gradio app
with gr.Blocks(css=css, theme=gr.themes.Soft(primary_hue="teal")) as demo:

    # Header 
    gr.HTML("""
    <div class="header-box">
        <div class="title">🌿 Soil Sensing and Recommendation Intelligence System</div>
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
                    nitrogen = gr.Number(label="N (mg/kg)", elem_classes="npk-input")
                    phosphorus = gr.Number(label="P (mg/kg)", elem_classes="npk-input")
                    potassium = gr.Number(label="K (mg/kg)", elem_classes="npk-input")

                with gr.Row():
                    submit_btn = gr.Button("Submit")
                    fetch_btn = gr.Button("Fetch Sensor Data")
        
        with gr.Column(scale=1):
            with gr.Group(elem_classes="snsdt"):
                gr.Markdown("## Upload Soil Image")
                image_input = gr.Image(label="Upload an image", type="pil")
                img_btn = gr.Button(" Analyze Image")

    with gr.Row(equal_height = True):
        
        with gr.Column(scale=1):
            with gr.Group(elem_classes="snsdt"):
                output = gr.Textbox(label="Predicted Soil Analysis / Recommendation", lines=2)
    
    with gr.Row():
        with gr.Column(scale=1) :
            with gr.Group(elem_classes="snsdt"):
                 chatbot = gr.Chatbot(label="Soil Advisor Chatbot",type="messages",height=300)
                 msg = gr.Textbox(label="Enter your message")
                 send_btn = gr.Button("Send")
                
                
    demo.launch()