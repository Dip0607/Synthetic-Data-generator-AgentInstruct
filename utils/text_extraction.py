import json
import time
from typing import List, Dict
import fitz
from docx import Document
import os

# Define chunk size as a constant
CHUNK_SIZE = 5000

def extract_text_chunks_from_file(file_path: str) -> List[str]:
    """
    Extract text chunks from a file based on its extension.

    Args:
    file_path (str): Path to the file.

    Returns:
    List[str]: List of text chunks.
    """
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.pdf':
        return extract_text_chunks_from_pdf(file_path)
    elif file_extension.lower() == '.docx':
        return extract_text_chunks_from_docx(file_path)
    elif file_extension.lower() in ['.txt', '.md']:
        return extract_text_chunks_from_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def extract_text_chunks_from_pdf(file_path: str) -> List[str]:
    """
    Extract text chunks from a PDF file.

    Args:
    file_path (str): Path to the PDF file.

    Returns:
    List[str]: List of text chunks.
    """
    pdf_document = fitz.open(file_path)
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]


def extract_text_chunks_from_docx(file_path: str) -> List[str]:
    """
    Extract text chunks from a DOCX file.

    Args:
    file_path (str): Path to the DOCX file.

    Returns:
    List[str]: List of text chunks.
    """
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]


def extract_text_chunks_from_text(file_path: str) -> List[str]:
    """
    Extract text chunks from a text file.

    Args:
    file_path (str): Path to the text file.

    Returns:
    List[str]: List of text chunks.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]


def parse_instruction_answer_pairs(text):
    pairs = []
    lines = text.strip().split('\n')
    instruction = ''
    answer = ''
    category = ''
    capturing_instruction = False
    capturing_answer = False
    capturing_category = False

    for line in lines:
        if line.strip().startswith('Question:'):
            capturing_instruction = True
            capturing_answer = False
            capturing_category = False
            instruction = line.replace('Question:', '').strip()
        elif line.strip().startswith('Answer:'):
            capturing_instruction = False
            capturing_answer = True
            capturing_category = False
            answer = line.replace('Answer:', '').strip()
        elif line.strip().startswith('Category:'):
            capturing_instruction = False
            capturing_answer = False
            capturing_category = True
            category = line.replace('Category:', '').strip()
        else:
            if capturing_instruction:
                instruction += ' ' + line.strip()
            elif capturing_answer:
                answer += ' ' + line.strip()
            elif capturing_category:
                category += ' ' + line.strip()

        # Append only when Question, Answer, and Category are complete
        if instruction and answer and category:
            pairs.append({
                'Question': instruction.strip(),
                'Answer': answer.strip(),
                'Category': category.strip()
            })
            instruction = ''
            answer = ''
            category = ''
            capturing_instruction = False
            capturing_answer = False
            capturing_category = False

    return pairs


def parse_refined_instruction_answer(text):
    """
    Parse the given text into Refined Question, Answer and Persona.

    Args:
    text (str): The input text containing Refined Question, Answer and Persona.

    Returns:
    dict or None: A dictionary containing 'Question', 'Answer' and 'Persona' if parsing is successful, otherwise None.
    """
    if text is None:
        return None  # or raise a custom error
    refined_instruction = ''
    refined_answer = ''
    persona = ''
    lines = text.strip().split('\n')
    capturing_instruction = False
    capturing_answer = False
    capturing_persona = False

    for line in lines:
        if line.strip().startswith('Refined Question:'):
            capturing_instruction = True
            capturing_answer = False
            capturing_persona = False
            refined_instruction = line.replace('Refined Question:', '').strip()
        elif line.strip().startswith('Refined Answer:'):
            capturing_instruction = False
            capturing_answer = True
            capturing_persona = False
            refined_answer = line.replace('Refined Answer:', '').strip()
        elif line.strip().startswith('Persona:'):
            capturing_instruction = False
            capturing_answer = False
            capturing_persona = True
            persona = line.replace('Persona:', '').strip()
        else:
            if capturing_instruction:
                refined_instruction += ' ' + line.strip()
            elif capturing_answer:
                refined_answer += ' ' + line.strip()
            elif capturing_persona:
                persona += ' ' + line.strip()

    if refined_instruction and refined_answer and persona:
        return {
            'Question': refined_instruction.strip(),
            'Answer': refined_answer.strip(),
            'Persona': persona.strip()
        }
    else:
        return None

