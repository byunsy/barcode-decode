@echo off
cls
echo Please scan the product's barcode. 
python html_gen.py
start chrome http://localhost:8000/results.html