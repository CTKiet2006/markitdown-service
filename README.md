# MarkItDown Microservice

FastAPI service wrapping Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) for converting various file formats to Markdown.

## Supported Formats
- PDF (with text layer)
- Word (DOCX)
- PowerPoint (PPTX)
- Excel (XLSX)
- HTML
- EPUB
- Images (with OCR)
- Audio (transcription)
- ZIP archives

## Quick Deploy on Render

1. Fork or use this repo
2. Create new Web Service on [Render](https://render.com)
3. Connect repo, runtime = **Docker**, plan = **Free**
4. Region: **Singapore**
5. Wait 2-5 minutes for build

Or use the included `render.yaml` (Infrastructure as Code).

## Local Development

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Test:
```bash
curl http://localhost:8000/health
curl -X POST -F "file=@test.docx" http://localhost:8000/convert
```

## API

### POST /convert
Upload a file (multipart/form-data, field name `file`).

Response:
```json
{
  "success": true,
  "markdown": "# Content...",
  "filename": "document.docx"
}
```

### GET /health
Returns `{"status": "ok", "service": "markitdown"}`

## Integration

In your Next.js / Vercel app, set environment variable:
```
MARKITDOWN_URL=https://your-markitdown-service.onrender.com
```
