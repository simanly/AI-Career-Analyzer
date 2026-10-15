from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from cv_parser import extract_text_from_pdf, extract_text_from_docx
from skills import extract_skills
from career_predictor import predict_careers, predict_resume_category
from skill_gap import calculate_skill_gap
from roadmap import generate_roadmap


app = FastAPI(title="AI Career Analyzer API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-career-analyzer-two.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI Career Analyzer API is running"}


@app.post("/analyze-cv")
async def analyze_cv(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File is required"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    temp_path = Path("temp_cv") / Path(file.filename).name
    temp_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        temp_path.write_bytes(file_bytes)

        if extension == ".pdf":
            text = extract_text_from_pdf(str(temp_path))
        else:
            text = extract_text_from_docx(str(temp_path))

        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the CV."
            )

        skills = extract_skills(text)
        careers = predict_careers(skills)

        try:
            ml_prediction = predict_resume_category(text)
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        skill_gap = calculate_skill_gap(careers)
        roadmap = generate_roadmap(skill_gap)

        return {
            "filename": file.filename,
            "text": text,
            "skills": skills,
            "careers": careers,
            "ml_prediction": ml_prediction,
            "skill_gap": skill_gap,
            "roadmap": roadmap
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"CV analysis failed: {str(exc)}"
        ) from exc
    finally:
        temp_path.unlink(missing_ok=True)