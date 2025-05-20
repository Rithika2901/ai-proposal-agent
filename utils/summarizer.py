from transformers import pipeline

# Use a better, faster model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_texts(text_list):
    combined_text = "\n".join(text_list)
    combined_text = combined_text[:4000]  # prevent overload

    chunks = [combined_text[i:i+1000] for i in range(0, len(combined_text), 1000)]
    summary_parts = []

    for chunk in chunks[:3]:  # limit to 3 chunks
        output = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
        summary_parts.append(output[0]['summary_text'])

    # Combine into proposal format
    proposal = "## Executive Summary\n"
    if len(summary_parts) > 0:
        proposal += summary_parts[0] + "\n\n"
    if len(summary_parts) > 1:
        proposal += "## Key Findings\n"
        proposal += "\n".join(f"- {s.strip()}" for s in summary_parts[1].split(".") if s.strip()) + "\n\n"
    if len(summary_parts) > 2:
        proposal += "## Recommendations\n"
        proposal += summary_parts[2]

    return proposal

