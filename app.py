from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import markitdown
import os
import tempfile

app = FastAPI(title="MarkItDown Service")

# CORS for your Vercel domain - update this with your actual domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set to your Vercel domain
    allow_methods=["POST"],
    allow_headers=["*"],
)

md = markitdown.MarkItDown()


@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    """Convert uploaded file to Markdown."""
    try:
        # Save to temp file
        suffix = os.path.splitext(file.filename or "")[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Convert using MarkItDown
        result = md.convert(tmp_path)

        # Cleanup
        os.unlink(tmp_path)

        return {
            "success": True,
            "markdown": result.text_content,
            "filename": file.filename,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "filename": file.filename,
        }


@app.get("/health")
async def health():
    return {"status": "ok", "service": "markitdown"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
