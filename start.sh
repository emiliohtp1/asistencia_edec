#!/bin/bash
echo "Iniciando servidor de Asistencia EDEC..."
echo ""
python -m uvicorn app.main:app --reload

