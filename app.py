
import os
import joblib
import pandas as pd

from io import BytesIO
from xml.sax.saxutils import escape

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from utils.preprocessing import FEATURES
from utils.recommendations import (
    get_career_info,
    get_skill_gap_analysis
)


# =====================================
# APP CONFIGURATION
# =====================================

app = Flask(__name__, static_folder="public", static_url_path="")

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "pathora-ai-development-secret-change-before-deployment"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "career_model.joblib"
)

model = None

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)


# =====================================
# HOME
# =====================================

@app.route("/")
def home():
    return render_template("index.html")


# =====================================
# CAREER PREDICTION
# =====================================

@app.route("/predict", methods=["POST"])
def predict():

    if model is None:
        return "Model not found. Run python train_model.py first.", 500

    try:

        student_data = {}

        for feature in FEATURES:

            value = float(request.form.get(feature, ""))

            if not 0 <= value <= 100:
                return f"Invalid value for {feature}. Enter 0 to 100.", 400

            student_data[feature] = value

        input_data = pd.DataFrame(
            [student_data],
            columns=FEATURES
        )

        prediction = str(model.predict(input_data)[0])

        scores = model.predict_proba(input_data)[0]

        ranked = sorted(
            zip(model.classes_, scores),
            key=lambda item: item[1],
            reverse=True
        )

        top_careers = [
            {
                "name": str(career),
                "score": round(float(score) * 100, 2)
            }
            for career, score in ranked[:3]
        ]

        career_info = get_career_info(prediction)

        skill_analysis = get_skill_gap_analysis(
            prediction,
            student_data
        )

        # Save latest analysis in session
        session["latest_analysis"] = {
            "prediction": prediction,
            "career_title": career_info["title"],
            "description": career_info["description"],
            "average_score": skill_analysis["average_score"],
            "strengths": skill_analysis["strengths"],
            "improvements": skill_analysis["improvements"],
            "top_careers": top_careers,
            "skills": career_info["skills"],
            "tools": career_info["tools"],
            "roadmap": career_info["roadmap"]
        }

        return render_template(
            "result.html",
            prediction=prediction,
            career_info=career_info,
            top_careers=top_careers,
            skill_analysis=skill_analysis
        )

    except (ValueError, TypeError):
        return "Please enter valid numeric values between 0 and 100.", 400


# =====================================
# RESULT PAGE
# =====================================

@app.route("/result")
def result_page():

    analysis = session.get("latest_analysis")

    if not analysis:
        return redirect(url_for("home"))

    career_info = get_career_info(analysis["prediction"])

    skill_analysis = {
        "average_score": analysis["average_score"],
        "strengths": analysis["strengths"],
        "improvements": analysis["improvements"]
    }

    return render_template(
        "result.html",
        prediction=analysis["prediction"],
        career_info=career_info,
        top_careers=analysis["top_careers"],
        skill_analysis=skill_analysis
    )


# =====================================
# CAREER ROADMAP
# =====================================

@app.route("/roadmap/<career>")
def roadmap(career):

    career_info = get_career_info(career)

    return render_template(
        "roadmap.html",
        career=career,
        career_info=career_info
    )


# =====================================
# ANALYTICS DASHBOARD
# =====================================

@app.route("/dashboard")
def dashboard():

    analysis = session.get("latest_analysis")

    return render_template(
        "dashboard.html",
        analysis=analysis
    )


# =====================================
# DOWNLOAD PDF REPORT
# =====================================

@app.route("/download-report")
def download_report():

    analysis = session.get("latest_analysis")

    if not analysis:
        return redirect(url_for("home"))

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#6544C5"),
        fontSize=23,
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#6544C5"),
        spaceBefore=16,
        spaceAfter=10
    )

    normal_style = styles["BodyText"]

    story = []

    story.append(Paragraph("PATHORA AI", title_style))
    story.append(Paragraph("Personalized Career Analysis Report", styles["Heading2"]))
    story.append(Spacer(1, 18))

    story.append(Paragraph(
        f"<b>Predicted Career:</b> {escape(analysis['career_title'])}",
        normal_style
    ))

    story.append(Spacer(1, 8))

    story.append(Paragraph(
        escape(analysis["description"]),
        normal_style
    ))

    story.append(Paragraph("Career Analytics", heading_style))

    story.append(Paragraph(
        f"<b>Overall Assessed Skill Score:</b> {analysis['average_score']}%",
        normal_style
    ))

    story.append(Paragraph("Top Career Recommendations", heading_style))

    career_data = [["Career", "Model Score"]]

    for career in analysis["top_careers"]:
        career_data.append([
            career["name"],
            f"{career['score']:.2f}%"
        ])

    career_table = Table(
        career_data,
        colWidths=[4 * inch, 1.5 * inch]
    )

    career_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6544C5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    story.append(career_table)

    story.append(Paragraph("Your Strengths", heading_style))

    if analysis["strengths"]:

        for skill in analysis["strengths"]:
            story.append(Paragraph(
                f"<b>{escape(skill['name'])}:</b> {skill['score']}%",
                normal_style
            ))
            story.append(Spacer(1, 5))

    else:
        story.append(Paragraph("No assessed strengths above the selected threshold.", normal_style))

    story.append(Paragraph("Skills to Improve", heading_style))

    if analysis["improvements"]:

        for skill in analysis["improvements"]:

            story.append(Paragraph(
                f"<b>{escape(skill['name'])}: {skill['score']}%</b>",
                normal_style
            ))

            story.append(Paragraph(
                escape(skill["suggestion"]),
                normal_style
            ))

            story.append(Spacer(1, 8))

    else:
        story.append(Paragraph("All assessed skills scored 70 or above.", normal_style))

    story.append(Paragraph("Recommended Career Skills", heading_style))

    story.append(Paragraph(
        escape(", ".join(analysis["skills"])),
        normal_style
    ))

    story.append(Paragraph("Recommended Tools", heading_style))

    story.append(Paragraph(
        escape(", ".join(analysis["tools"])),
        normal_style
    ))

    story.append(Paragraph("Career Roadmap", heading_style))

    for index, step in enumerate(analysis["roadmap"], start=1):

        story.append(Paragraph(
            f"{index}. {escape(step)}",
            normal_style
        ))

        story.append(Spacer(1, 5))

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "<b>Disclaimer:</b> This report provides educational "
        "Machine Learning-based recommendations. It is not a "
        "professional career assessment or a guarantee of future success.",
        normal_style
    ))

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "Generated by Pathora AI | 2026",
        styles["Italic"]
    ))

    document.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Pathora_AI_Career_Report.pdf",
        mimetype="application/pdf"
    )


# =====================================
# RUN APPLICATION
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
