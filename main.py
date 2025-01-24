from typing import Dict, Union
import markdown2
import markdown_text
from fpdf import FPDF
from html.parser import HTMLParser


class PDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        # Load regular and bold DejaVu fonts (for Unicode + bold support)
        self.add_font("DejaVu", "", "fonts/DejaVuSansCondensed.ttf", uni=True)
        self.add_font("DejaVu", "B", "fonts/DejaVuSansCondensed-Bold.ttf", uni=True)

        # Basic PDF setup
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font("DejaVu", size=12)

    def add_html_content(self, html_content: str):
        class HTMLToPDFParser(HTMLParser):
            def __init__(self, pdf):
                super().__init__()
                self.pdf = pdf
                self.in_code_block = False

                # Track current font state
                self.current_font = {
                    "family": "DejaVu",
                    "style": "",
                    "size": 12
                }

            def set_font_from_tag(self, tag):
                """Apply an inline style change based on the HTML tag."""
                if tag in ("strong", "b"):
                    # Bold style
                    self.current_font["style"] += "B"
                elif tag in ("em", "i"):
                    # Italic style
                    self.current_font["style"] += "I"
                elif tag == "code":
                    # Inline code in Courier (no auto-bold to avoid 'BB' error)
                    self.current_font["family"] = "Courier"
                    self.current_font["style"] = ""
                    self.current_font["size"] = 12

                self.pdf.set_font(
                    self.current_font["family"],
                    self.current_font["style"],
                    self.current_font["size"]
                )

            def reset_font(self, tag):
                """Reset the style change when the tag ends."""
                if tag in ("strong", "b"):
                    self.current_font["style"] = self.current_font["style"].replace("B", "")
                elif tag in ("em", "i"):
                    self.current_font["style"] = self.current_font["style"].replace("I", "")
                elif tag == "code":
                    # Return to normal DejaVu font
                    self.current_font["family"] = "DejaVu"
                    self.current_font["size"] = 12

                # Re-apply the current font setting
                self.pdf.set_font(
                    self.current_font["family"],
                    self.current_font["style"],
                    self.current_font["size"]
                )

            def handle_starttag(self, tag, attrs):
                """Handle block/inline elements at the start."""
                # Headings
                if tag in ("h1", "h2", "h3"):
                    sizes = {"h1": 16, "h2": 14, "h3": 12}
                    self.pdf.ln(6)
                    self.pdf.set_font("DejaVu", "B", sizes[tag])

                # Block tags
                elif tag in ("p", "ul", "ol"):
                    self.pdf.ln(5)

                elif tag == "li":
                    self.pdf.ln(5)
                    self.pdf.write(5, u"\u2022 ")  # bullet

                # Inline style tags (bold, italic, code)
                elif tag in ("strong", "b", "em", "i", "code"):
                    self.set_font_from_tag(tag)

                # Multi-line code block: <pre>
                if tag == "pre":
                    self.pdf.ln(5)
                    # Courier (no bold) at smaller size
                    self.pdf.set_font("Courier", "", 11)
                    self.pdf.set_fill_color(240, 240, 240)
                    self.in_code_block = True

            def handle_endtag(self, tag):
                """When a tag ends, revert style if needed."""
                if tag in ("h1", "h2", "h3"):
                    self.pdf.ln(5)
                    # Return to normal DejaVu
                    self.pdf.set_font("DejaVu", "", 12)

                elif tag in ("strong", "b", "em", "i", "code"):
                    self.reset_font(tag)

                elif tag == "pre":
                    self.pdf.ln(5)
                    self.pdf.set_font("DejaVu", "", 12)
                    self.pdf.set_fill_color(255, 255, 255)
                    self.in_code_block = False

            def handle_data(self, data):
                """Handle the text data inside tags."""
                if self.in_code_block:
                    # Preserve newlines in code blocks
                    lines = data.splitlines()
                    for line in lines:
                        self.pdf.multi_cell(0, 5, line, fill=True)
                else:
                    # Inline text: collapse newlines to spaces
                    text = data.replace("\n", " ")
                    if text.strip():
                        self.pdf.write(5, text + " ")

        parser = HTMLToPDFParser(self)
        parser.feed(html_content)

    def add_markdown_content(self, markdown_content: str):
        """Convert Markdown to HTML, then parse it."""
        html_content = markdown2.markdown(
            markdown_content,
            extras=["fenced-code-blocks", "tables", "code-friendly"]
        )
        self.add_html_content(html_content)

def pdf_creator_tool(
    markdown_content: str,
    filename: str = "output.pdf",
    bucket_name: str = "pdf_storage"
) -> Dict[str, Union[bool, str]]:
    """
    Convert the provided Markdown content into a PDF,
    upload it to Supabase Storage, and return a public link.
    """
    try:
        if not markdown_content.strip():
            return {"success": False, "error": "Markdown content is empty."}

        pdf = PDFGenerator()
        pdf.add_markdown_content(markdown_content)
        pdf.output(filename)

        return {
            "success": True,
            "message": "PDF created successfully.",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
   
    result = pdf_creator_tool(markdown_text.markdown_content) 
    print(result)
