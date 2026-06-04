from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter


def format_content(value):
    """
    Converte listas, strings ou valores nulos
    para texto compatível com Paragraph.
    """

    if value is None:
        return "Não informado"

    if isinstance(value, list):
        return "<br/>".join(
            f"• {item}" for item in value
        )

    return str(value)


def generate_pdf(analysis):

    document = SimpleDocTemplate(
        buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1565F0")
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Heading3"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555")
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#1565F0"),
        spaceAfter=10
    )

    result_style = ParagraphStyle(
        "ResultStyle",
        parent=styles["BodyText"],
        textColor=colors.HexColor("#0B8043"),
        fontSize=12,
        leading=20
    )

    body_style = styles["BodyText"]

    elements = []

    elements.append(
        Paragraph(
            "BIO LENS",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "Relatório Inteligente de Análise de Possíveis Focos de Dengue",
            subtitle_style
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.grey
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "1. Informações da Ocorrência",
            section_style
        )
    )

    identificacao = f"""
    <b>Bairro:</b> {analysis.get('bairro', 'Não informado')}<br/>
    <b>Local:</b> {analysis.get('local', 'Não informado')}<br/>
    <b>Data da Foto:</b> {analysis.get('data_foto', 'Não informado')}<br/>
    """

    if analysis.get("localizacao"):
        identificacao += f"""
        <b>Latitude:</b> {analysis['localizacao'].get('latitude')}<br/>
        <b>Longitude:</b> {analysis['localizacao'].get('longitude')}<br/>
        """

    elements.append(
        Paragraph(
            identificacao,
            body_style
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "3. Resultado da Classificação",
            section_style
        )
    )

    resultado = f"""
    <b>Resultado:</b> {analysis.get('resultado', 'Não informado')}<br/>
    <b>Classe Detectada:</b> {analysis.get('classe', 'Não informado')}<br/>
    <b>Confiança da IA:</b> {analysis.get('confianca', 0)}%<br/>
    """

    elements.append(
        Paragraph(
            resultado,
            result_style
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "4. Descrição da Ocorrência",
            section_style
        )
    )

    elements.append(
        Paragraph(
            format_content(
                analysis.get("descricao")
            ),
            body_style
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "5. Avaliação de Risco",
            section_style
        )
    )

    elements.append(
        Paragraph(
            format_content(
                analysis.get("risco")
            ),
            body_style
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "6. Recomendações Preventivas",
            section_style
        )
    )

    elements.append(
        Paragraph(
            format_content(
                analysis.get("prevencao")
            ),
            body_style
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "7. Orientações Técnicas",
            section_style
        )
    )

    elements.append(
        Paragraph(
            format_content(
                analysis.get("orientacao")
            ),
            body_style
        )
    )

    elements.append(Spacer(1, 25))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.grey
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            """
            <b>Bio Lens</b><br/>
            Relatório gerado automaticamente por Inteligência Artificial.<br/>
            Este documento tem caráter informativo e auxilia ações de monitoramento,
            prevenção e combate a possíveis focos do mosquito <i>Aedes aegypti</i>.
            """,
            body_style
        )
    )

    document.build(elements)
    buffer.seek(0)

    return buffer