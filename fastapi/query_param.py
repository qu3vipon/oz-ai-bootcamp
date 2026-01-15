from fastapi import FastAPI, Query


app = FastAPI()

# Query Parameter: ?{key}={value}
@app.get("/search")
def search_api(q: str = Query(default="default", min_length=2, max_length=8)):
    return {"msg": f"searched: {q}"}


# GET /users/3/posts?limit=10   -> 3번 사용자의 게시물 10개 조회
@app.get("/users/{user_id}/posts")
def list_posts_api(user_id: int, limit: int):
    # Path -> 자원(리소스)을 식별 
    # Query -> 조회 옵션
    
    # URL 경로 상에 존재하면 Path, 없으면 Query
    return {"user_id": user_id, "limit": limit}


# 검색 API 만들기
# GET /products/search?q=apple&limit=5
# 응답: {"q": "apple", "limit": 5}
@app.get("/products/search")
def product_search_api(
    q: str = Query(..., max_length=6),
    limit: int = Query(..., ge=3),
):
    return (q, limit)
