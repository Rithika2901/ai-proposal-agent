from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

def summarize_texts(text_list):
    combined_text = "\n".join(text_list)
    chunks = [combined_text[i:i+1000] for i in range(0, len(combined_text), 1000)]
    summary_parts = []

    for chunk in chunks:
        output = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
        summary_parts.append(output[0]['summary_text'])

    proposal = "## Executive Summary\n"
    proposal += summary_parts[0] + "\n\n"

    if len(summary_parts) > 1:
        proposal += "## Key Findings\n"
        proposal += "\n".join(f"- {s.strip()}" for s in summary_parts[1].split(".") if s.strip()) + "\n\n"

    if len(summary_parts) > 2:
        proposal += "## Recommendations\n"
        proposal += summary_parts[2]

    return proposal
