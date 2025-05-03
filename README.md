# DIP0607 Synthetic Data Generator - AgentInstruct

A tool for generating synthetic instruction data using AI agents, leveraging AutoGen and OpenAI models.

## Overview

This project implements an agent-based approach to synthetic data generation, specifically focused on creating high-quality instruction data for AI training. The system uses multiple specialized agents that work together to generate, refine, and validate instruction data.

## Directory Structure

```
dip0607-synthetic-data-generator-agentinstruct/
├── README.md                  # This documentation file
├── chunk_1_output.json        # Sample output data
├── main.py                    # Entry point for the application
├── Personas_single.txt        # Persona definitions for instruction generation
├── requirements.txt           # Project dependencies
├── agents/                    # Agent implementations
│   ├── agent_configs.json     # Configuration for different agents
│   ├── base_agent.py          # Base class for all agents
│   ├── instruction_generation.py  # Agent for generating initial instructions
│   └── instruction_refinement.py  # Agent for refining generated instructions
└── utils/
    └── text_extraction.py     # Utility functions for text processing
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dip0607-synthetic-data-generator-agentinstruct.git
cd dip0607-synthetic-data-generator-agentinstruct
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY=your_api_key_here  # On Windows: set OPENAI_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

Run the main script to generate synthetic instruction data:

```bash
python main.py
```

### Advanced Usage

You can customize the generation process by passing additional arguments:

```bash
python main.py --num_instructions 100 --output_file custom_output.json --persona_file custom_personas.txt
```

## Configuration

### Agent Configuration

Agent behaviors are configured in the `agents/agent_configs.json` file. You can modify this file to adjust parameters like:
- Model selection
- Temperature settings
- Maximum token limits
- Agent-specific parameters

Example configuration:
```json
{
  "instruction_generator": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1024
  },
  "instruction_refiner": {
    "model": "gpt-4",
    "temperature": 0.3,
    "max_tokens": 1024
  }
}
```

### Personas

The system uses personas defined in `Personas_single.txt` to guide the instruction generation process. Each persona represents a different type of user with specific characteristics, needs, and communication styles.

## Components

### Agents

- **Base Agent (`base_agent.py`)**: Defines the common functionality for all agents.
- **Instruction Generation Agent (`instruction_generation.py`)**: Creates initial instruction data based on personas and requirements.
- **Instruction Refinement Agent (`instruction_refinement.py`)**: Reviews and improves the generated instructions to ensure quality.

### Utilities

- **Text Extraction (`utils/text_extraction.py`)**: Provides functionality for extracting and processing text from various sources.

## Output Format

The generated instructions are saved in JSON format, as demonstrated in `chunk_1_output.json`. Each entry typically contains:
- The instruction text
- Metadata about the generation process
- Any associated contexts or examples

## Requirements

The project dependencies are listed in `requirements.txt` and include:
- AutoGen
- OpenAI API client
- Various utility libraries

## Extending the Project

### Adding New Agents

1. Create a new agent file in the `agents/` directory
2. Inherit from the `BaseAgent` class
3. Implement the required methods
4. Add configuration settings in `agent_configs.json`
5. Update `main.py` to include the new agent in the workflow

### Customizing Personas

Edit the `Personas_single.txt` file to add, modify, or remove personas. Each persona should include:
- Demographic information
- Communication style
- Interests and expertise
- Typical needs and queries

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your OpenAI API key is correctly set as an environment variable.
2. **Rate Limiting**: If you encounter rate limits, adjust the processing speed in the configuration.
3. **Out of Memory**: For large generation tasks, consider processing in smaller batches.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Specify your license here]

## Acknowledgments

- This project utilizes the AutoGen framework for multi-agent orchestration
- OpenAI models power the intelligent generation capabilities
