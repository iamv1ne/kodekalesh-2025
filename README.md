Kuch Toota?

Real-time defect detection using Advanced Canny Edge Detection.

# Problem
Manual inspection = 30% error rate → $10M recalls

->Solution
- Upload image
- RED BOX = DEFECT
- BLUE BOX = GOOD
- CPU-only. Real-time. No training.
-(demo images provided are of bottles)

->Tech Stack:
- OpenCV: Canny + Bilateral Filter + Morphology
- Streamlit
- Python

-> Run
   bash
   python -m streamlit run app.py

->Future:
-Scalable to CCTV Cameras.
-Can Use a large dataset and implement ML, using pretrained YOLO model.
-Can work at dark stores in blinkit, zepto, etc. to check whether a certain product is broken or not.
