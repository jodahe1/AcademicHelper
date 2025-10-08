# n8n Workflows

This directory contains exported n8n workflows for the Academic Assignment Helper system.

## Files

- `assignment_analysis_workflow.json` - Main workflow for processing assignments

## How to Import

1. Access n8n at `http://localhost:5678`
2. Login with credentials: `admin` / `admin123`
3. Click "+" to create new workflow
4. Click the "..." menu → "Import from file"
5. Select the JSON file from this directory
6. Configure any required credentials (OpenAI/Gemini API keys)
7. Activate the workflow

## Workflow Overview

The assignment analysis workflow includes:

1. **Webhook Trigger** - Receives assignment data from FastAPI
2. **Text Extraction** - Processes PDF/DOCX files
3. **RAG Search** - Queries vector database for relevant sources
4. **AI Analysis** - Generates research suggestions and plagiarism detection
5. **Data Storage** - Saves results to PostgreSQL

## Configuration Required

After importing, configure:
- API credentials for OpenAI/Gemini
- Database connection settings
- Webhook URLs

## Troubleshooting

If the workflow fails to import:
1. Ensure n8n is running and accessible
2. Check that all required nodes are available
3. Verify the JSON file is not corrupted
4. Try importing individual nodes if full workflow import fails
