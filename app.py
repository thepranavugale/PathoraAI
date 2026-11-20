
# # import os
# # import joblib
# # import pandas as pd

# # from io import BytesIO
# # from xml.sax.saxutils import escape

# # from flask import (
# #     Flask,
# #     render_template,
# #     request,
# #     redirect,
# #     url_for,
# #     session,
# #     send_file
# # )

# # from reportlab.lib import colors
# # from reportlab.lib.pagesizes import A4
# # from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# # from reportlab.lib.units import inch
# # from reportlab.platypus import (
# #     SimpleDocTemplate,
# #     Paragraph,
# #     Spacer,
# #     Table,
# #     TableStyle
# # )

# # from utils.preprocessing import FEATURES
# # from utils.recommendations import (
# #     get_career_info,
# #     get_skill_gap_analysis
# # )


# # # =====================================
# # # APP CONFIGURATION
# # # =====================================

# # app = Flask(__name__, static_folder="public", static_url_path="")

# # app.secret_key = os.environ.get(
# #     "SECRET_KEY",
# #     "pathora-ai-development-secret-change-before-deployment"
# # )

# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # MODEL_PATH = os.path.join(
# #     BASE_DIR, "models", "career_model.joblib"
# # )

# # model = None

# # if os.path.exists(MODEL_PATH):
# #     model = joblib.load(MODEL_PATH)


# # # =====================================
# # # HOME
# # # =====================================

# # @app.route("/")
# # def home():
# #     return render_template("index.html")


# # # =====================================
# # # CAREER PREDICTION
# # # =====================================

# # @app.route("/predict", methods=["POST"])
# # def predict():

# #     if model is None:
# #         return "Model not found. Run python train_model.py first.", 500

# #     try:

# #         student_data = {}

# #         for feature in FEATURES:

# #             value = float(request.form.get(feature, ""))

# #             if not 0 <= value <= 100:
# #                 return f"Invalid value for {feature}. Enter 0 to 100.", 400

# #             student_data[feature] = value

# #         input_data = pd.DataFrame(
# #             [student_data],
# #             columns=FEATURES
# #         )

# #         prediction = str(model.predict(input_data)[0])

# #         scores = model.predict_proba(input_data)[0]

# #         ranked = sorted(
# #             zip(model.classes_, scores),
# #             key=lambda item: item[1],
# #             reverse=True
# #         )

# #         top_careers = [
# #             {
# #                 "name": str(career),
# #                 "score": round(float(score) * 100, 2)
# #             }
# #             for career, score in ranked[:3]
# #         ]

# #         career_info = get_career_info(prediction)

# #         skill_analysis = get_skill_gap_analysis(
# #             prediction,
# #             student_data
# #         )

# #         # Save latest analysis in session
# #         session["latest_analysis"] = {
# #             "prediction": prediction,
# #             "career_title": career_info["title"],
# #             "description": career_info["description"],
# #             "average_score": skill_analysis["average_score"],
# #             "strengths": skill_analysis["strengths"],
# #             "improvements": skill_analysis["improvements"],
# #             "top_careers": top_careers,
# #             "skills": career_info["skills"],
# #             "tools": career_info["tools"],
# #             "roadmap": career_info["roadmap"]
# #         }

# #         return render_template(
# #             "result.html",
# #             prediction=prediction,
# #             career_info=career_info,
# #             top_careers=top_careers,
# #             skill_analysis=skill_analysis
# #         )

# #     except (ValueError, TypeError):
# #         return "Please enter valid numeric values between 0 and 100.", 400


# # # =====================================
# # # RESULT PAGE
# # # =====================================

# # @app.route("/result")
# # def result_page():

# #     analysis = session.get("latest_analysis")

# #     if not analysis:
# #         return redirect(url_for("home"))

# #     career_info = get_career_info(analysis["prediction"])

# #     skill_analysis = {
# #         "average_score": analysis["average_score"],
# #         "strengths": analysis["strengths"],
# #         "improvements": analysis["improvements"]
# #     }

# #     return render_template(
# #         "result.html",
# #         prediction=analysis["prediction"],
# #         career_info=career_info,
# #         top_careers=analysis["top_careers"],
# #         skill_analysis=skill_analysis
# #     )


# # # =====================================
# # # CAREER ROADMAP
# # # =====================================

# # @app.route("/roadmap/<career>")
# # def roadmap(career):

# #     career_info = get_career_info(career)

# #     return render_template(
# #         "roadmap.html",
# #         career=career,
# #         career_info=career_info
# #     )


# # # =====================================
# # # ANALYTICS DASHBOARD
# # # =====================================

# # @app.route("/dashboard")
# # def dashboard():

# #     analysis = session.get("latest_analysis")

# #     return render_template(
# #         "dashboard.html",
# #         analysis=analysis
# #     )


# # # =====================================
# # # DOWNLOAD PDF REPORT
# # # =====================================

# # @app.route("/download-report")
# # def download_report():

# #     analysis = session.get("latest_analysis")

# #     if not analysis:
# #         return redirect(url_for("home"))

# #     buffer = BytesIO()

# #     document = SimpleDocTemplate(
# #         buffer,
# #         pagesize=A4,
# #         rightMargin=45,
# #         leftMargin=45,
# #         topMargin=45,
# #         bottomMargin=45
# #     )

# #     styles = getSampleStyleSheet()

# #     title_style = ParagraphStyle(
# #         "ReportTitle",
# #         parent=styles["Title"],
# #         textColor=colors.HexColor("#6544C5"),
# #         fontSize=23,
# #         spaceAfter=12
# #     )

# #     heading_style = ParagraphStyle(
# #         "ReportHeading",
# #         parent=styles["Heading2"],
# #         textColor=colors.HexColor("#6544C5"),
# #         spaceBefore=16,
# #         spaceAfter=10
# #     )

# #     normal_style = styles["BodyText"]

# #     story = []

# #     story.append(Paragraph("PATHORA AI", title_style))
# #     story.append(Paragraph("Personalized Career Analysis Report", styles["Heading2"]))
# #     story.append(Spacer(1, 18))

# #     story.append(Paragraph(
# #         f"<b>Predicted Career:</b> {escape(analysis['career_title'])}",
# #         normal_style
# #     ))

# #     story.append(Spacer(1, 8))

# #     story.append(Paragraph(
# #         escape(analysis["description"]),
# #         normal_style
# #     ))

# #     story.append(Paragraph("Career Analytics", heading_style))

# #     story.append(Paragraph(
# #         f"<b>Overall Assessed Skill Score:</b> {analysis['average_score']}%",
# #         normal_style
# #     ))

# #     story.append(Paragraph("Top Career Recommendations", heading_style))

# #     career_data = [["Career", "Model Score"]]

# #     for career in analysis["top_careers"]:
# #         career_data.append([
# #             career["name"],
# #             f"{career['score']:.2f}%"
# #         ])

# #     career_table = Table(
# #         career_data,
# #         colWidths=[4 * inch, 1.5 * inch]
# #     )

# #     career_table.setStyle(TableStyle([
# #         ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6544C5")),
# #         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
# #         ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
# #         ("PADDING", (0, 0), (-1, -1), 9),
# #         ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
# #     ]))

# #     story.append(career_table)

# #     story.append(Paragraph("Your Strengths", heading_style))

# #     if analysis["strengths"]:

# #         for skill in analysis["strengths"]:
# #             story.append(Paragraph(
# #                 f"<b>{escape(skill['name'])}:</b> {skill['score']}%",
# #                 normal_style
# #             ))
# #             story.append(Spacer(1, 5))

# #     else:
# #         story.append(Paragraph("No assessed strengths above the selected threshold.", normal_style))

# #     story.append(Paragraph("Skills to Improve", heading_style))

# #     if analysis["improvements"]:

# #         for skill in analysis["improvements"]:

# #             story.append(Paragraph(
# #                 f"<b>{escape(skill['name'])}: {skill['score']}%</b>",
# #                 normal_style
# #             ))

# #             story.append(Paragraph(
# #                 escape(skill["suggestion"]),
# #                 normal_style
# #             ))

# #             story.append(Spacer(1, 8))

# #     else:
# #         story.append(Paragraph("All assessed skills scored 70 or above.", normal_style))

# #     story.append(Paragraph("Recommended Career Skills", heading_style))

# #     story.append(Paragraph(
# #         escape(", ".join(analysis["skills"])),
# #         normal_style
# #     ))

# #     story.append(Paragraph("Recommended Tools", heading_style))

# #     story.append(Paragraph(
# #         escape(", ".join(analysis["tools"])),
# #         normal_style
# #     ))

# #     story.append(Paragraph("Career Roadmap", heading_style))

# #     for index, step in enumerate(analysis["roadmap"], start=1):

# #         story.append(Paragraph(
# #             f"{index}. {escape(step)}",
# #             normal_style
# #         ))

# #         story.append(Spacer(1, 5))

# #     story.append(Spacer(1, 20))

# #     story.append(Paragraph(
# #         "<b>Disclaimer:</b> This report provides educational "
# #         "Machine Learning-based recommendations. It is not a "
# #         "professional career assessment or a guarantee of future success.",
# #         normal_style
# #     ))

# #     story.append(Spacer(1, 20))

# #     story.append(Paragraph(
# #         "Generated by Pathora AI | 2026",
# #         styles["Italic"]
# #     ))

# #     document.build(story)

# #     buffer.seek(0)

# #     return send_file(
# #         buffer,
# #         as_attachment=True,
# #         download_name="Pathora_AI_Career_Report.pdf",
# #         mimetype="application/pdf"
# #     )


# # # =====================================
# # # RUN APPLICATION
# # # =====================================

# # if __name__ == "__main__":
# #     app.run(debug=True)





# import os
# import joblib
# import pandas as pd

# from io import BytesIO
# from xml.sax.saxutils import escape

# from flask import (
#     Flask,
#     render_template,
#     request,
#     redirect,
#     url_for,
#     session,
#     send_file
# )

# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Paragraph,
#     Spacer,
#     Table,
#     TableStyle
# )

# from utils.preprocessing import FEATURES
# from utils.recommendations import (
#     get_career_info,
#     get_skill_gap_analysis
# )


# # =====================================
# # 1. APP CONFIGURATION
# # =====================================

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# app = Flask(
#     __name__,
#     static_folder="public",
#     static_url_path=""
# )

# SECRET_KEY = os.environ.get("SECRET_KEY")

# if not SECRET_KEY:
#     if os.environ.get("VERCEL"):
#         raise RuntimeError(
#             "SECRET_KEY environment variable is missing!"
#         )
#     SECRET_KEY = "local-development-only-secret"

# app.secret_key = SECRET_KEY

# app.config.update(
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE="Lax",
#     SESSION_COOKIE_SECURE=bool(os.environ.get("VERCEL"))
# )


# # =====================================
# # 2. MODEL CONFIGURATION
# # =====================================

# MODEL_PATH = os.path.join(
#     BASE_DIR,
#     "models",
#     "career_model.joblib"
# )

# model = None

# try:
#     if os.path.exists(MODEL_PATH):
#         model = joblib.load(MODEL_PATH)
#         print("Career ML Model loaded successfully!")
#     else:
#         print("WARNING: Career model not found:", MODEL_PATH)

# except Exception as error:
#     print("Model loading error:", error)


# # =====================================
# # 3. HOME PAGE
# # =====================================

# @app.route("/")
# def home():
#     return render_template("index.html")


# # =====================================
# # 4. CAREER PREDICTION
# # =====================================

# @app.route("/predict", methods=["POST"])
# def predict():

#     if model is None:
#         return "Career model not found. Check models/career_model.joblib.", 500

#     try:

#         student_data = {}

#         for feature in FEATURES:

#             raw_value = request.form.get(feature)

#             if raw_value is None or raw_value.strip() == "":
#                 return f"Missing input: {feature}", 400

#             value = float(raw_value)

#             if not 0 <= value <= 100:
#                 return f"Invalid value for {feature}. Enter 0 to 100.", 400

#             student_data[feature] = value

#         input_data = pd.DataFrame(
#             [student_data],
#             columns=FEATURES
#         )

#         # Predict career
#         prediction = str(model.predict(input_data)[0])

#         # Get model scores
#         if hasattr(model, "predict_proba"):
#             probabilities = model.predict_proba(input_data)[0]

#             ranked = sorted(
#                 zip(model.classes_, probabilities),
#                 key=lambda item: item[1],
#                 reverse=True
#             )

#         else:
#             ranked = [(prediction, 1.0)]

#         top_careers = [
#             {
#                 "name": str(career),
#                 "score": round(float(score) * 100, 2)
#             }
#             for career, score in ranked[:3]
#         ]

#         # Career information
#         career_info = get_career_info(prediction)

#         # Skill gap analysis
#         skill_analysis = get_skill_gap_analysis(
#             prediction,
#             student_data
#         )

#         # Save analysis in session
#         session["latest_analysis"] = {
#             "prediction": prediction,
#             "career_title": career_info["title"],
#             "description": career_info["description"],
#             "average_score": skill_analysis["average_score"],
#             "strengths": skill_analysis["strengths"],
#             "improvements": skill_analysis["improvements"],
#             "top_careers": top_careers,
#             "skills": career_info["skills"],
#             "tools": career_info["tools"],
#             "roadmap": career_info["roadmap"]
#         }

#         session.modified = True

#         return render_template(
#             "result.html",
#             prediction=prediction,
#             career_info=career_info,
#             top_careers=top_careers,
#             skill_analysis=skill_analysis
#         )

#     except (ValueError, TypeError):
#         return "Please enter valid numeric values between 0 and 100.", 400

#     except Exception as error:
#         app.logger.exception("Career prediction failed")
#         return f"Prediction error: {str(error)}", 500


# # =====================================
# # 5. RESULT PAGE
# # =====================================

# @app.route("/result")
# def result_page():

#     analysis = session.get("latest_analysis")

#     if not analysis:
#         return redirect(url_for("home"))

#     career_info = get_career_info(
#         analysis["prediction"]
#     )

#     skill_analysis = {
#         "average_score": analysis["average_score"],
#         "strengths": analysis["strengths"],
#         "improvements": analysis["improvements"]
#     }

#     return render_template(
#         "result.html",
#         prediction=analysis["prediction"],
#         career_info=career_info,
#         top_careers=analysis["top_careers"],
#         skill_analysis=skill_analysis
#     )


# # =====================================
# # 6. CAREER ROADMAP
# # =====================================

# @app.route("/roadmap/<career>")
# def roadmap(career):

#     career_info = get_career_info(career)

#     return render_template(
#         "roadmap.html",
#         career=career,
#         career_info=career_info
#     )


# # =====================================
# # 7. ANALYTICS DASHBOARD
# # =====================================

# @app.route("/dashboard")
# def dashboard():

#     analysis = session.get("latest_analysis")

#     return render_template(
#         "dashboard.html",
#         analysis=analysis
#     )


# # =====================================
# # 8. DOWNLOAD PDF REPORT
# # =====================================

# @app.route("/download-report")
# def download_report():

#     analysis = session.get("latest_analysis")

#     if not analysis:
#         return redirect(url_for("home"))

#     buffer = BytesIO()

#     document = SimpleDocTemplate(
#         buffer,
#         pagesize=A4,
#         rightMargin=45,
#         leftMargin=45,
#         topMargin=45,
#         bottomMargin=45
#     )

#     styles = getSampleStyleSheet()

#     title_style = ParagraphStyle(
#         "ReportTitle",
#         parent=styles["Title"],
#         textColor=colors.HexColor("#6544C5"),
#         fontSize=23,
#         spaceAfter=12
#     )

#     heading_style = ParagraphStyle(
#         "ReportHeading",
#         parent=styles["Heading2"],
#         textColor=colors.HexColor("#6544C5"),
#         spaceBefore=16,
#         spaceAfter=10
#     )

#     normal_style = styles["BodyText"]

#     story = []

#     story.append(
#         Paragraph("PATHORA AI", title_style)
#     )

#     story.append(
#         Paragraph(
#             "Personalized Career Analysis Report",
#             styles["Heading2"]
#         )
#     )

#     story.append(Spacer(1, 18))

#     story.append(
#         Paragraph(
#             f"<b>Predicted Career:</b> "
#             f"{escape(str(analysis['career_title']))}",
#             normal_style
#         )
#     )

#     story.append(Spacer(1, 8))

#     story.append(
#         Paragraph(
#             escape(str(analysis["description"])),
#             normal_style
#         )
#     )

#     # Career analytics
#     story.append(
#         Paragraph("Career Analytics", heading_style)
#     )

#     story.append(
#         Paragraph(
#             f"<b>Overall Assessed Skill Score:</b> "
#             f"{analysis['average_score']}%",
#             normal_style
#         )
#     )

#     # Top career recommendations
#     story.append(
#         Paragraph(
#             "Top Career Recommendations",
#             heading_style
#         )
#     )

#     career_data = [
#         ["Career", "Model Score"]
#     ]

#     for career_item in analysis["top_careers"]:

#         career_data.append([
#             str(career_item["name"]),
#             f"{career_item['score']:.2f}%"
#         ])

#     career_table = Table(
#         career_data,
#         colWidths=[4 * inch, 1.5 * inch]
#     )

#     career_table.setStyle(
#         TableStyle([
#             (
#                 "BACKGROUND",
#                 (0, 0),
#                 (-1, 0),
#                 colors.HexColor("#6544C5")
#             ),
#             (
#                 "TEXTCOLOR",
#                 (0, 0),
#                 (-1, 0),
#                 colors.white
#             ),
#             (
#                 "GRID",
#                 (0, 0),
#                 (-1, -1),
#                 0.5,
#                 colors.grey
#             ),
#             (
#                 "PADDING",
#                 (0, 0),
#                 (-1, -1),
#                 9
#             ),
#             (
#                 "VALIGN",
#                 (0, 0),
#                 (-1, -1),
#                 "MIDDLE"
#             )
#         ])
#     )

#     story.append(career_table)

#     # Strengths
#     story.append(
#         Paragraph("Your Strengths", heading_style)
#     )

#     if analysis["strengths"]:

#         for skill in analysis["strengths"]:

#             story.append(
#                 Paragraph(
#                     f"<b>{escape(str(skill['name']))}:</b> "
#                     f"{skill['score']}%",
#                     normal_style
#                 )
#             )

#             story.append(Spacer(1, 5))

#     else:

#         story.append(
#             Paragraph(
#                 "No assessed strengths above the selected threshold.",
#                 normal_style
#             )
#         )

#     # Improvements
#     story.append(
#         Paragraph("Skills to Improve", heading_style)
#     )

#     if analysis["improvements"]:

#         for skill in analysis["improvements"]:

#             story.append(
#                 Paragraph(
#                     f"<b>{escape(str(skill['name']))}: "
#                     f"{skill['score']}%</b>",
#                     normal_style
#                 )
#             )

#             story.append(
#                 Paragraph(
#                     escape(str(skill["suggestion"])),
#                     normal_style
#                 )
#             )

#             story.append(Spacer(1, 8))

#     else:

#         story.append(
#             Paragraph(
#                 "All assessed skills scored 70 or above.",
#                 normal_style
#             )
#         )

#     # Recommended skills
#     story.append(
#         Paragraph(
#             "Recommended Career Skills",
#             heading_style
#         )
#     )

#     story.append(
#         Paragraph(
#             escape(", ".join(map(str, analysis["skills"]))),
#             normal_style
#         )
#     )

#     # Recommended tools
#     story.append(
#         Paragraph(
#             "Recommended Tools",
#             heading_style
#         )
#     )

#     story.append(
#         Paragraph(
#             escape(", ".join(map(str, analysis["tools"]))),
#             normal_style
#         )
#     )

#     # Roadmap
#     story.append(
#         Paragraph("Career Roadmap", heading_style)
#     )

#     for index, step in enumerate(
#         analysis["roadmap"],
#         start=1
#     ):

#         story.append(
#             Paragraph(
#                 f"{index}. {escape(str(step))}",
#                 normal_style
#             )
#         )

#         story.append(Spacer(1, 5))

#     # Disclaimer
#     story.append(Spacer(1, 20))

#     story.append(
#         Paragraph(
#             "<b>Disclaimer:</b> This report provides educational "
#             "Machine Learning-based recommendations. It is not a "
#             "professional career assessment or a guarantee of future success.",
#             normal_style
#         )
#     )

#     story.append(Spacer(1, 20))

#     story.append(
#         Paragraph(
#             "Generated by Pathora AI | 2026",
#             styles["Italic"]
#         )
#     )

#     document.build(story)

#     buffer.seek(0)

#     return send_file(
#         buffer,
#         as_attachment=True,
#         download_name="Pathora_AI_Career_Report.pdf",
#         mimetype="application/pdf"
#     )


# # =====================================
# # 9. HEALTH CHECK
# # =====================================

# @app.route("/health")
# def health():

#     return {
#         "status": "running",
#         "application": "Pathora AI",
#         "model_loaded": model is not None
#     }


# # =====================================
# # 10. RUN LOCAL SERVER
# # =====================================

# if __name__ == "__main__":

#     app.run(
#         host="127.0.0.1",
#         port=5000,
#         debug=True
#     )






















import os
import logging
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
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
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


# ==========================================
# 1. APPLICATION CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder="public",
    static_url_path=""
)

app.logger.setLevel(logging.INFO)

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    if os.environ.get("VERCEL"):
        raise RuntimeError(
            "SECRET_KEY environment variable is missing!"
        )

    SECRET_KEY = "local-development-only-secret"

app.secret_key = SECRET_KEY

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=bool(os.environ.get("VERCEL")),
    MAX_CONTENT_LENGTH=10 * 1024 * 1024
)


# ==========================================
# 2. MACHINE LEARNING MODEL
# ==========================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "career_model.joblib"
)

model = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        app.logger.info("Career ML Model loaded successfully!")
    else:
        app.logger.error(
            "Career model not found: %s",
            MODEL_PATH
        )

except Exception:
    app.logger.exception("Error loading career model")


# ==========================================
# 3. HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# 4. CAREER PREDICTION
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    if model is None:
        app.logger.error("Prediction requested but model is unavailable.")
        return "Career model is unavailable. Please try again later.", 500

    try:
        student_data = {}

        for feature in FEATURES:

            raw_value = request.form.get(feature)

            if raw_value is None or raw_value.strip() == "":
                return f"Missing input: {feature}", 400

            value = float(raw_value)

            if not 0 <= value <= 100:
                return (
                    f"Invalid value for {feature}. Enter 0 to 100.",
                    400
                )

            student_data[feature] = value

        input_data = pd.DataFrame(
            [student_data],
            columns=FEATURES
        )

        # Predict career
        prediction = str(model.predict(input_data)[0])

        # Calculate career probabilities
        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(input_data)[0]

            ranked = sorted(
                zip(model.classes_, probabilities),
                key=lambda item: item[1],
                reverse=True
            )

        else:
            ranked = [(prediction, 1.0)]

        top_careers = [
            {
                "name": str(career),
                "score": round(float(score) * 100, 2)
            }
            for career, score in ranked[:3]
        ]

        # Career information
        career_info = get_career_info(prediction)

        # Skill gap analysis
        skill_analysis = get_skill_gap_analysis(
            prediction,
            student_data
        )

        # Save analysis in Flask session
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

        session.modified = True

        return render_template(
            "result.html",
            prediction=prediction,
            career_info=career_info,
            top_careers=top_careers,
            skill_analysis=skill_analysis
        )

    except (ValueError, TypeError):
        return (
            "Please enter valid numeric values between 0 and 100.",
            400
        )

    except Exception:
        app.logger.exception("Career prediction failed")
        return "An error occurred during prediction.", 500


# ==========================================
# 5. RESULT PAGE
# ==========================================

@app.route("/result")
def result_page():

    analysis = session.get("latest_analysis")

    if not analysis:
        return redirect(url_for("home"))

    career_info = get_career_info(
        analysis["prediction"]
    )

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


# ==========================================
# 6. CAREER ROADMAP
# ==========================================

@app.route("/roadmap/<career>")
def roadmap(career):

    career_info = get_career_info(career)

    return render_template(
        "roadmap.html",
        career=career,
        career_info=career_info
    )


# ==========================================
# 7. ANALYTICS DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    analysis = session.get("latest_analysis")

    return render_template(
        "dashboard.html",
        analysis=analysis
    )


# ==========================================
# 8. DOWNLOAD PDF REPORT
# ==========================================

@app.route("/download-report")
def download_report():

    analysis = session.get("latest_analysis")

    if not analysis:
        return redirect(url_for("home"))

    try:
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

        # Report title
        story.append(
            Paragraph("PATHORA AI", title_style)
        )

        story.append(
            Paragraph(
                "Personalized Career Analysis Report",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 18))

        # Predicted career
        story.append(
            Paragraph(
                f"<b>Predicted Career:</b> "
                f"{escape(str(analysis['career_title']))}",
                normal_style
            )
        )

        story.append(Spacer(1, 8))

        story.append(
            Paragraph(
                escape(str(analysis["description"])),
                normal_style
            )
        )

        # Career analytics
        story.append(
            Paragraph("Career Analytics", heading_style)
        )

        story.append(
            Paragraph(
                f"<b>Overall Assessed Skill Score:</b> "
                f"{analysis['average_score']}%",
                normal_style
            )
        )

        # Top careers
        story.append(
            Paragraph(
                "Top Career Recommendations",
                heading_style
            )
        )

        career_data = [
            ["Career", "Model Score"]
        ]

        for career_item in analysis["top_careers"]:

            career_data.append([
                str(career_item["name"]),
                f"{career_item['score']:.2f}%"
            ])

        career_table = Table(
            career_data,
            colWidths=[4 * inch, 1.5 * inch]
        )

        career_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#6544C5")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    9
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                )
            ])
        )

        story.append(career_table)

        # Strengths
        story.append(
            Paragraph("Your Strengths", heading_style)
        )

        if analysis["strengths"]:

            for skill in analysis["strengths"]:

                story.append(
                    Paragraph(
                        f"<b>{escape(str(skill['name']))}:</b> "
                        f"{skill['score']}%",
                        normal_style
                    )
                )

                story.append(Spacer(1, 5))

        else:

            story.append(
                Paragraph(
                    "No assessed strengths above the selected threshold.",
                    normal_style
                )
            )

        # Improvements
        story.append(
            Paragraph("Skills to Improve", heading_style)
        )

        if analysis["improvements"]:

            for skill in analysis["improvements"]:

                story.append(
                    Paragraph(
                        f"<b>{escape(str(skill['name']))}: "
                        f"{skill['score']}%</b>",
                        normal_style
                    )
                )

                story.append(
                    Paragraph(
                        escape(str(skill["suggestion"])),
                        normal_style
                    )
                )

                story.append(Spacer(1, 8))

        else:

            story.append(
                Paragraph(
                    "All assessed skills scored 70 or above.",
                    normal_style
                )
            )

        # Recommended skills
        story.append(
            Paragraph(
                "Recommended Career Skills",
                heading_style
            )
        )

        story.append(
            Paragraph(
                escape(", ".join(map(str, analysis["skills"]))),
                normal_style
            )
        )

        # Recommended tools
        story.append(
            Paragraph(
                "Recommended Tools",
                heading_style
            )
        )

        story.append(
            Paragraph(
                escape(", ".join(map(str, analysis["tools"]))),
                normal_style
            )
        )

        # Career roadmap
        story.append(
            Paragraph("Career Roadmap", heading_style)
        )

        for index, step in enumerate(
            analysis["roadmap"],
            start=1
        ):

            story.append(
                Paragraph(
                    f"{index}. {escape(str(step))}",
                    normal_style
                )
            )

            story.append(Spacer(1, 5))

        # Disclaimer
        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Disclaimer:</b> This report provides educational "
                "Machine Learning-based recommendations. It is not a "
                "professional career assessment or a guarantee of future success.",
                normal_style
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "Generated by Pathora AI | 2026",
                styles["Italic"]
            )
        )

        document.build(story)

        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="Pathora_AI_Career_Report.pdf",
            mimetype="application/pdf"
        )

    except Exception:
        app.logger.exception("PDF report generation failed")
        return "Unable to generate the PDF report.", 500


# ==========================================
# 9. HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return {
        "status": "running",
        "application": "Pathora AI",
        "model_loaded": model is not None
    }


# ==========================================
# 10. LOCAL DEVELOPMENT
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
