from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


def generate_pdf(path, analysis):

    document = SimpleDocTemplate(
        path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Relatório de Análise de Dengue",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    content = f"""
    <b>Bairro:</b> {analysis['bairro']}<br/>
    <b>Local:</b> {analysis['local']}<br/>
    <b>Data da Foto:</b> {analysis['data_foto']}<br/>
    <b>Resultado:</b> {analysis['resultado']}<br/>
    <b>Confiança:</b> {analysis['confianca']}%<br/>
    """

    paragraph = Paragraph(
        content,
        styles["BodyText"]
    )

    elements.append(paragraph)

    document.build(elements)