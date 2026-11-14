# اجرا
## بک‌اند
cd backend
python -m venv .venv && source .venv/bin/activate   # ویندوز: .venv\Scripts\activate
pip install -r requirements.txt
# در .env مقدار BEATAPI_API_KEY و APP_TOKEN و توضیحات خودت را بگذار
uvicorn app.main:app --host 0.0.0.0 --port 8000
# تست: http://localhost:8000/api/health  و  /docs

## فرانت‌اند
ng new frontend --standalone --skip-tests
# chat.service.ts و app.component.ts را در frontend/src/app/ کپی کن
ng serve --host 0.0.0.0
