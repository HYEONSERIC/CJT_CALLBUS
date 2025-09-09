from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Quote
from .schemas import QuoteInitIn, QuoteOut

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CALLBUS API")

# 프론트가 file:// 또는 127.0.0.1에서 접근할 수 있도록 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 필요시 도메인으로 좁히세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

# 1) 초기 저장: 고객 유형/목적 저장 → quoteId 반환
@app.post("/api/quotes/init", response_model=QuoteOut)
def create_quote(payload: QuoteInitIn, db: Session = Depends(get_db)):
    qid = str(uuid4())
    q = Quote(
        id=qid,
        customer_type=payload.customerType,
        purpose=payload.purpose,
        step=1
    )
    db.add(q)
    db.commit()
    return {"quoteId": qid}

# 2) 다음 단계에서 날짜/출발/도착 업데이트 (선택)
from pydantic import BaseModel
class QuoteWhenWhereIn(BaseModel):
    date: str
    depart: str
    arrive: str

@app.post("/api/quotes/{quote_id}/when-where")
def save_when_where(quote_id: str, payload: QuoteWhenWhereIn, db: Session = Depends(get_db)):
    q = db.get(Quote, quote_id)
    if not q:
        raise HTTPException(404, "Quote not found")
    # 필요시 별도 테이블로 분리; 여기서는 간단히 step만 진행
    q.step = 2
    db.commit()
    return {"ok": True, "next": "passenger-info"}
