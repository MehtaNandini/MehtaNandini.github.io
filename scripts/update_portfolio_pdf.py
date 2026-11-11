from __future__ import annotations

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


PAGE_WIDTH, PAGE_HEIGHT = letter
BLUE = HexColor("#27679F")
DARK = HexColor("#18344D")
TEXT = HexColor("#344653")
MUTED = HexColor("#5F6D76")
PANEL = HexColor("#EEF3F7")
LINE = HexColor("#B8C9D5")


def draw_wrapped_text(
    pdf: canvas.Canvas,
    text: str,
    *,
    x: float,
    y: float,
    max_width: float,
    font: str,
    size: float,
    leading: float,
    color: HexColor = TEXT,
) -> float:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and pdf.stringWidth(candidate, font, size) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)

    pdf.setFont(font, size)
    pdf.setFillColor(color)
    for line in lines:
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_section_heading(pdf: canvas.Canvas, text: str, y: float) -> None:
    pdf.setFillColor(BLUE)
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(44, y, text)
    pdf.setStrokeColor(BLUE)
    pdf.setLineWidth(0.7)
    pdf.line(44, y - 10, 568, y - 10)


def draw_fitted_image(
    pdf: canvas.Canvas, image_path: Path, *, x: float, y: float, width: float, height: float
) -> None:
    image = ImageReader(str(image_path))
    image_width, image_height = image.getSize()
    scale = min(width / image_width, height / image_height)
    drawn_width = image_width * scale
    drawn_height = image_height * scale
    pdf.setFillColor(white)
    pdf.rect(x, y, width, height, fill=1, stroke=0)
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.45)
    pdf.rect(x, y, width, height, fill=0, stroke=1)
    pdf.drawImage(
        image,
        x + (width - drawn_width) / 2,
        y + (height - drawn_height) / 2,
        width=drawn_width,
        height=drawn_height,
        preserveAspectRatio=True,
        mask="auto",
    )


def create_energyml_page(output: Path, screenshots: Path) -> None:
    pdf = canvas.Canvas(str(output), pagesize=letter, pageCompression=1)
    pdf.setTitle("EnergyML Research Platform - Portfolio Project")

    pdf.setFillColor(BLUE)
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(44, 752, "ENERGY SYSTEMS MACHINE LEARNING")
    pdf.setStrokeColor(BLUE)
    pdf.setLineWidth(0.7)
    pdf.line(44, 740, 568, 740)

    pdf.setFillColor(PANEL)
    pdf.rect(44, 539, 524, 177, fill=1, stroke=0)
    pdf.setFillColor(BLUE)
    pdf.rect(44, 539, 2.6, 177, fill=1, stroke=0)

    pdf.setFont("Times-Roman", 12)
    pdf.drawString(56, 694, "10")
    pdf.setFillColor(DARK)
    pdf.setFont("Times-Roman", 10.5)
    pdf.drawString(84, 694, "Machine Learning and Energy Systems")
    pdf.setFont("Times-Roman", 15)
    pdf.drawString(56, 665, "EnergyML Research Platform")

    pdf.setFont("Times-Bold", 7.9)
    pdf.drawString(56, 627, "Technologies:")
    pdf.setFont("Times-Roman", 7.9)
    pdf.drawString(
        105,
        627,
        "Python | FastAPI | scikit-learn | PostgreSQL | SQLAlchemy | Docker Compose",
    )

    pdf.setFont("Times-Bold", 8.1)
    pdf.drawString(56, 597, "Impact:")
    draw_wrapped_text(
        pdf,
        "Built a reproducible research platform from deterministic energy data through held-out model evaluation, artifact verification and validated inference.",
        x=88,
        y=597,
        max_width=460,
        font="Times-Roman",
        size=8.1,
        leading=10,
    )

    bullets = [
        "Generated 8,760 hourly renewable observations and 5,000 five-bus network samples.",
        "Reduced forecasting MAE by 37.6 percent versus a 24-hour persistence baseline.",
        "Achieved 0.000269 p.u. voltage-estimation MAE with hashed artifacts and API inference.",
    ]
    bullet_y = 566
    pdf.setFillColor(TEXT)
    for bullet in bullets:
        pdf.setFont("Times-Roman", 8)
        pdf.drawString(58, bullet_y, "-")
        draw_wrapped_text(
            pdf,
            bullet,
            x=68,
            y=bullet_y,
            max_width=484,
            font="Times-Roman",
            size=8,
            leading=9,
        )
        bullet_y -= 10

    draw_section_heading(pdf, "PLATFORM WORKFLOW", 508)
    workflow = [
        ("GENERATE", "seeded data"),
        ("ENGINEER", "safe features"),
        ("TRAIN", "ML pipelines"),
        ("VERIFY", "metrics + hashes"),
        ("SERVE", "FastAPI"),
    ]
    box_y, box_h, box_w, gap = 448, 42, 96, 10
    for index, (title, detail) in enumerate(workflow):
        box_x = 44 + index * (box_w + gap)
        pdf.setFillColor(PANEL)
        pdf.roundRect(box_x, box_y, box_w, box_h, 4, fill=1, stroke=0)
        pdf.setFillColor(DARK)
        pdf.setFont("Times-Roman", 8.4)
        pdf.drawCentredString(box_x + box_w / 2, box_y + 25, title)
        pdf.setFillColor(MUTED)
        pdf.setFont("Times-Roman", 7)
        pdf.drawCentredString(box_x + box_w / 2, box_y + 11, detail)
        if index < len(workflow) - 1:
            pdf.setFillColor(BLUE)
            pdf.setFont("Times-Roman", 10)
            pdf.drawCentredString(box_x + box_w + gap / 2, box_y + 21, ">")

    draw_section_heading(pdf, "WORKING PRODUCT", 414)
    image_y, image_h, image_w = 235, 130, 168
    image_specs = [
        ("01-overview.jpg", "Overview and registry counts"),
        ("03-experiments.jpg", "Completed experiments"),
        ("05-inference.jpg", "Active-model inference"),
    ]
    for index, (filename, caption) in enumerate(image_specs):
        image_x = 44 + index * 178
        draw_fitted_image(
            pdf,
            screenshots / filename,
            x=image_x,
            y=image_y,
            width=image_w,
            height=image_h,
        )
        pdf.setFillColor(DARK)
        pdf.setFont("Times-Roman", 8.3)
        pdf.drawCentredString(image_x + image_w / 2, 221, caption)

    pdf.setFillColor(PANEL)
    pdf.roundRect(44, 142, 524, 54, 4, fill=1, stroke=0)
    pdf.setFillColor(DARK)
    pdf.setFont("Times-Roman", 9.6)
    pdf.drawString(56, 175, "Reproducible research from seeded data to active-model inference")
    pdf.setFillColor(MUTED)
    pdf.setFont("Times-Roman", 7.8)
    pdf.drawString(
        56,
        157,
        "2 datasets | 2 completed experiments | 2 active models | 19 tests | Docker/PostgreSQL",
    )

    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.55)
    pdf.line(44, 55, 568, 55)
    pdf.setFillColor(MUTED)
    pdf.setFont("Times-Roman", 7.5)
    pdf.drawString(44, 39, "Nandini Mehta | Software Engineering Portfolio")
    pdf.drawRightString(568, 39, "Project 10 / 10")
    pdf.showPage()
    pdf.save()


def footer_overlay(project_number: int) -> PdfReader:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFillColor(white)
    pdf.rect(517, 30, 57, 20, fill=1, stroke=0)
    pdf.setFillColor(MUTED)
    pdf.setFont("Times-Roman", 7.5)
    pdf.drawRightString(568, 37.4, f"Project {project_number:02d} / 10")
    pdf.save()
    buffer.seek(0)
    return PdfReader(buffer)


def build_portfolio(source: Path, output: Path, screenshots: Path, working_dir: Path) -> None:
    working_dir.mkdir(parents=True, exist_ok=True)
    energyml_page = working_dir / "energyml-project-page.pdf"
    create_energyml_page(energyml_page, screenshots)

    reader = PdfReader(str(source))
    if len(reader.pages) != 10:
        raise ValueError(f"Expected 10 source pages, found {len(reader.pages)}")

    writer = PdfWriter()
    for index, page in enumerate(reader.pages[:9], start=1):
        page.merge_page(footer_overlay(index).pages[0], over=True)
        writer.add_page(page)
    writer.add_page(PdfReader(str(energyml_page)).pages[0])
    writer.add_page(reader.pages[9])

    metadata = {key: str(value) for key, value in (reader.metadata or {}).items() if value}
    metadata["/Title"] = "Nandini Mehta - Software Engineering Portfolio"
    metadata["/Subject"] = "Software engineering, data systems, enterprise AI and energy ML delivery"
    metadata["/Author"] = "Nandini Mehta"
    writer.add_metadata(metadata)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as stream:
        writer.write(stream)

    verified = PdfReader(str(output))
    if len(verified.pages) != 11:
        raise ValueError(f"Expected 11 output pages, found {len(verified.pages)}")


if __name__ == "__main__":
    workspace = Path(__file__).resolve().parents[1]
    build_portfolio(
        source=Path(
            "/Users/nandini/Desktop/Nandini_Documents/Fulltime/"
            "Nandini Fulltime Documents/Portfolio/NandiniMehta_Portfolio.pdf"
        ),
        output=workspace / "output" / "pdf" / "NandiniMehta_Portfolio_EnergyML.pdf",
        screenshots=workspace / "public" / "projects" / "energyml" / "dashboard-captures",
        working_dir=workspace / "tmp" / "pdfs" / "final",
    )
