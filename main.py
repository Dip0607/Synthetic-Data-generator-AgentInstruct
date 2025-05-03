import json
import openai
import os
from utils.text_extraction import extract_text_chunks_from_file
from agents.base_agent import BaseAgent
from agents.instruction_generation import generate_instructions
from agents.instruction_refinement import refine_instructions 
import sys
import time
import argparse
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

openai.api_type = "azure"
openai.api_base = " https://<your-endpoint>.openai.azure.com/"
openai.api_version = "2024-03-01-preview"
openai.api_key = "  <your-key>"
openai.azure_endpoint = "https://<your-endpoint>.openai.azure.com/"

def load_agent_configs():
    with open('agents/agent_configs.json', 'r') as json_file:
        return json.load(json_file)

def content_transformation_flow(text, agent_configs):
    transformed_contents = []
    for config in agent_configs:
        agent = BaseAgent(
            name=config['name'],
            system_prompt=config['system_prompt'],
            user_prompt_template=config['user_prompt_template']
        )
        agent_output = agent.process(text)
        if agent_output:
            transformed_contents.extend(agent_output)
    return transformed_contents


def get_embedding(text):
    return openai.embeddings.create(input=text, model="genaiembeddingmodel").data[0].embedding


def remove_semantic_duplicates(instructions, similarity_threshold=0.90):
    unique_instructions = []
    embeddings = []

    for instruction in instructions:
        question = instruction.get('Question', '')
        answer = instruction.get('answer', '')
        combined_text = question + " " + answer
        embedding = get_embedding(combined_text)

        is_duplicate = False
        for idx, existing_embedding in enumerate(embeddings):
            similarity = cosine_similarity([embedding], [existing_embedding])[0][0]
            if similarity > similarity_threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            unique_instructions.append(instruction)
            embeddings.append(embedding)

    return unique_instructions


def process_file(file_path, persona, agent_configs):
    start_time = time.time()

    # Step 1: Extract text chunks
    text_chunks = extract_text_chunks_from_file(file_path)
    print(f"Number of text chunks extracted from {file_path}: {len(text_chunks)}")

    dataset = []
    total_refined_instructions = 0

    for chunk_index, text in enumerate(text_chunks):
        chunk_start_time = time.time()
        print(f"Processing chunk {chunk_index + 1}/{len(text_chunks)}...")

        # Step 2: Improved Content Transformation
        transformed_contents = content_transformation_flow(text, agent_configs)
        print(f"Number of transformed contents: {len(transformed_contents)}")

        # Step 3: Seed Instruction Generation
        instructions = generate_instructions(transformed_contents)
        print(f"Number of questions generated: {len(instructions)}")

        # Step 4: Instruction Refinement (now with persona)
        refined_instructions = refine_instructions(instructions, persona)
        print(f"Number of refined questions: {len(refined_instructions)}")

        total_refined_instructions += len(refined_instructions)
        dataset.extend(refined_instructions)

        chunk_end_time = time.time()
        chunk_duration = chunk_end_time - chunk_start_time
        print(f"Chunk {chunk_index + 1} processing time: {chunk_duration:.2f} seconds")

    # Remove semantic duplicates from the dataset
    unique_dataset = remove_semantic_duplicates(dataset)
    unique_instructions_count = len(unique_dataset)

    end_time = time.time()
    total_duration = end_time - start_time

    print(f"File processing complete for {file_path}")
    print(f"Total processing time for {file_path}: {total_duration:.2f} seconds")
    print(f"Total refined questions for {file_path}: {total_refined_instructions}")
    print(f"Unique questions after removing semantic duplicates: {unique_instructions_count}")

    return unique_dataset, unique_instructions_count



def main(file_paths, persona_file_path):
    start_time = time.time()

    # Load agent configurations
    agent_configs = load_agent_configs()

    # Load persona
    persona = extract_text_chunks_from_file(persona_file_path)
    print(f"Loaded persona: {persona}")

    all_datasets = []
    total_unique_instructions = 0
    file_summaries = []

    for file_path in file_paths:
        print(f"\nProcessing file: {file_path}")
        dataset, file_unique_instructions = process_file(file_path, persona, agent_configs)
        all_datasets.extend(dataset)
        total_unique_instructions += file_unique_instructions
        
        file_summaries.append({
            "file_name": os.path.basename(file_path),
            "unique_questions": file_unique_instructions
        })

    # Remove semantic duplicates from the combined dataset
    final_dataset = remove_semantic_duplicates(all_datasets)
    final_unique_instructions_count = len(final_dataset)

    # Prepare the final output
    final_output = {
        "total_unique_questions": final_unique_instructions_count,
        "file_summaries": file_summaries,
        "datasets": final_dataset
    }

    # Save the complete dataset to a single JSON file
    output_file = "combined_synthetic_dataset.json"
    with open(output_file, 'w') as f:
        json.dump(final_output, f, indent=4)

    end_time = time.time()
    total_duration = end_time - start_time

    print(f"\nAll files processed. Combined dataset saved to {output_file}")
    print(f"Total unique questions across all files: {final_unique_instructions_count}")
    print(f"Total processing time for all files: {total_duration:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process multiple input files and generate a synthetic dataset.")
    parser.add_argument("input_files", nargs="+", help="Paths to input files")
    parser.add_argument("persona_file", help="Path to persona file")
    args = parser.parse_args()

    script_start_time = time.time()
    main(args.input_files, args.persona_file)
    script_end_time = time.time()
    script_duration = script_end_time - script_start_time

    print(f"Total script execution time: {script_duration:.2f} seconds")