import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    HRFlowable
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter

from app.config.config import Config


def generate_pdf(path, analysis):

    document = SimpleDocTemplate(
        path,
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
        textColor=colors.HexColor("#0F4C81")
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Heading3"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#444444")
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#0F4C81"),
        spaceAfter=10
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
            "Sistema Inteligente de Identificação de Possíveis Focos de Dengue",
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
            "1. Identificação da Ocorrência",
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

    image_name = analysis.get("imagem")

    if image_name:

        image_path = os.path.join(
            Config.UPLOAD_FOLDER,
            image_name
        )

        if os.path.exists(image_path):

            elements.append(
                Paragraph(
                    "2. Imagem Analisada",
                    section_style
                )
            )

            try:

                img = Image(
                    image_path,
                    width=300,
                    height=220
                )

                elements.append(img)

            except Exception:
                pass

            elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "3. Resultado da Classificação",
            section_style
        )
    )

    resultado = f"""
    <b>Resultado:</b> {analysis.get('resultado', 'Não informado')}<br/>
    <b>Classe:</b> {analysis.get('classe', 'Não informado')}<br/>
    <b>Nível de Confiança:</b> {analysis.get('confianca', 0)}%<br/>
    """

    elements.append(
        Paragraph(
            resultado,
            body_style
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
            analysis.get(
                "descricao",
                "Descrição não disponível."
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
            analysis.get(
                "risco",
                "Não informado."
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
            analysis.get(
                "prevencao",
                "Nenhuma recomendação disponível."
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
            analysis.get(
                "orientacao",
                "Nenhuma orientação disponível."
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
            Este documento auxilia ações de monitoramento, prevenção e combate a possíveis focos do mosquito Aedes aegypti.
            """,
            body_style
        )
    )

    document.build(elements)