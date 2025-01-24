# PDF Generator

A Python project that converts Markdown content into PDFs using `FPDF` and `markdown2`. Managed with [UV](https://docs.astral.sh/uv/), a fast and efficient Python package manager.

## Project Structure

```
project-root/
├── fonts/
│   ├── DejaVuSansCondensed.ttf
│   └── DejaVuSansCondensed-Bold.ttf
├── .env
├── .gitignore
├── .python-version
├── main.py
├── markdown_text.py
├── output.pdf
├── pyproject.toml
├── README.md
├── uv.lock
```

- **fonts/**: Contains the DejaVu fonts used for Unicode and bold text support in PDFs.
- **main.py**: The main script that drives the PDF generation process.
- **markdown_text.py**: Contains the Markdown content to be converted to a PDF.
- **output.pdf**: The generated PDF file.
- **README.md**: This file, providing an overview of the project.
- **pyproject.toml**: Configuration file for managing project dependencies with UV.
- **uv.lock**: Tracks installed dependencies for reproducibility.

## Features

- Converts Markdown content to PDF.
- Supports Unicode characters and basic text formatting.
- Utilizes DejaVu fonts for better character rendering.
- Handles code blocks, headings, bullet lists, and inline styles like bold/italic text.

## Requirements

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) package manager

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/pdf-generator.git
   cd pdf-generator
   ```

2. **Install UV** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Set Up the Project Environment**:

   UV will automatically create a virtual environment and install dependencies specified in `pyproject.toml`.

   ```bash
   uv sync
   ```

## Usage

1. **Prepare Your Markdown Content**:

   Edit the `markdown_text.py` file to include your desired Markdown content.

2. **Run the PDF Generator**:

   ```bash
   uv run main.py
   ```

   This will generate an `output.pdf` in the project directory.

## Adding Dependencies

To add new dependencies to the project, use UV:

```bash
uv add package_name
```

For example, to add `requests`:

```bash
uv add requests
```

This will update the `pyproject.toml` file and install the package in your project's virtual environment. ([docs.astral.sh](https://docs.astral.sh/uv/guides/projects/?utm_source=chatgpt.com))

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Built With

- [FPDF](http://www.fpdf.org/) for PDF generation.
- [markdown2](https://github.com/trentm/python-markdown2) for Markdown to HTML conversion.
- [UV](https://docs.astral.sh/uv/) for efficient project and dependency management.

## Acknowledgements

- **Author**: Muhammad Raffey
- **Portfolio**: [Muhammad Raffey's Portfolio](https://raffey-portfolio.vercel.app/)
- **LinkedIn**: [linkedin.com/in/muhammadraffey](https://www.linkedin.com/in/muhammadraffey)
