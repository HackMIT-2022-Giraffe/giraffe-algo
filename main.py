from dotenv import load_dotenv
import os
from pdf.pdf import PDF

if __name__ == "__main__":
    load_dotenv()

    print(os.getenv('GPT3_API_KEY'))

    pdf = PDF('data/test_pdf.pdf', 5, api_key=os.getenv('GPT3_API_KEY'))
    pdf.generateTranscript()