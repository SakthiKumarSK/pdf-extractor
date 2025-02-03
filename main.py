!pip install pypdf
from pypdf import PdfReader

import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

pdf_text_content = []

reader = PdfReader("/content/SJS Transcript Call.pdf")
for i in range(len(reader.pages)):
  page = reader.pages[i]
  page_content = page.extract_text()
  pdf_text_content.append(page_content)

merged_pdf_text = "\n".join(pdf_text_content)

# Process text with spaCy
doc = nlp(merged_pdf_text)

# Define the target speaker
target_speakers = ["Devanshi Dhruva", "Ronak Mehta", "Mahendra Naredi", "Sanjay Thapar", "K.A. Joseph"]
# Extract and print only the text for the target speaker
print(f"Statements by {target_speakers}:")
target_text = []
capture = False

## to find keyword
for line in merged_pdf_text.splitlines():
    line = line.strip()
    # Check if the line starts with the target speaker's name
    if any(line.startswith(f"{speaker}:") for speaker in target_speakers):
        # Start capturing if we find the target speaker's line
        capture = True
        target_text.append(line.split(":", 1)[1].strip())  # Skip the name part
    elif line and not line.split(":")[0] in [ "Moderator", "Amit Hiranandani", "Ridhima Goyal", "Piyush Parag", "Karn Bhargava", "Shrinjana Mittal", "Rohan Advant", "Vishal Khurana"]:
        # Continue capturing text if it’s a continuation of the target speaker's answer
        if capture:
            target_text.append(line)
    else:
        # Stop capturing when another speaker is found
        capture = False

# Join and display the extracted content
print("\n".join(target_text))

doc1 = nlp("\n".join(target_text))

keywords = ["growth", "investment","future","business"]
print("\nKey Sentences:")
for sent in doc1.sents:
    if any(keyword in sent.text.lower() for keyword in keywords):
        print(sent.text)
