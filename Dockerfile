FROM python:3.10
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-spa

RUN TESSDATA_VERSION=$(ls /usr/share/tesseract-ocr/ | grep -E '^.*$') && \
    echo "TESSDATA_PREFIX=/usr/share/tesseract-ocr/${TESSDATA_VERSION}/tessdata/" >> /etc/environment

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm
EXPOSE 8080
CMD ["uvicorn", "lecto:app", "--host", "0.0.0.0", "--port", "8080"]
