from transformers import pipeline
import gradio as gr

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analysis_sentiment(text):
    result = classifier(text)[0]

    return {
        result["label"] : result["score"]
    }

# Interface gradio

demo = gr.Interface(
    fn=analysis_sentiment,
    inputs=gr.Textbox(
        label="Entrez votre texte",
        lines=3
    ),
    outputs=gr.Label(
        label="Résultat"
    ),
    title="Analyse de sentiment",
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch()