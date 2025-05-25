from fastapi import APIRouter, Query, HTTPException, Depends, status, Body
from config.database import db
from models.post_helper import post_helper
from typing import List,Optional
from schemas.post import PostOut, PostCreate, PostUpdate, CommentCreate, CommentOut 
from bson import ObjectId
from auth.dependencies import get_current_user
from datetime import datetime, timezone, timedelta
import uuid
from pymongo import ReturnDocument 

IST = timezone(timedelta(hours=5, minutes=30))

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[PostOut])
async def get_all_posts(search: str = Query(None)):
    query = {}
    if search:
        query = {
            "$or": [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}}
            ]
        }

    posts_cursor = db.posts.find(query)
    posts = await posts_cursor.to_list(length=100)
    return [post_helper(post) for post in posts]

@router.get("/user", response_model=List[PostOut])
async def get_user_posts(current_user: str = Depends(get_current_user)):
    posts_cursor = db.posts.find({"author_email": current_user["email"]})
    posts = await posts_cursor.to_list(length=100)
    return [post_helper(post) for post in posts]


# Add a comment
@router.post("/{post_id}/comments", response_model=CommentOut)
async def add_comment(
    post_id: str,
    comment: CommentCreate,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment_id = str(uuid.uuid4())
    comment_data = {
        "id": comment_id,
        "author_email": current_user["email"],
        "author_name": current_user.get("name", "Unknown"),
        "text": comment.text,
        "date": datetime.now(IST)
    }

    update_result = await db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments": comment_data}}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to add comment")

    return comment_data


@router.delete("/{post_id}/comments/{comment_id}")
async def delete_comment(
    post_id: str,
    comment_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment_to_delete = None
    for comment in post.get("comments", []):
        if comment["id"] == comment_id:
            comment_to_delete = comment
            break

    if not comment_to_delete:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment_to_delete["author_email"] != current_user["email"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    result = await db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$pull": {"comments": {"id": comment_id}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete comment")

    return {"detail": "Comment deleted successfully"}

# Toggle like/unlike post
@router.post("/{post_id}/like")
async def toggle_like(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    likes = post.get("likes", [])
    user_email = current_user["email"]

    if user_email in likes:
        # Unlike
        likes.remove(user_email)
    else:
        # Like
        likes.append(user_email)

    update_result = await db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"likes": likes}}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update likes")

    return {"likes_count": len(likes), "liked": user_email in likes}


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: str):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    post = await db.posts.find_one_and_update(
        {"_id": ObjectId(post_id)},
        {"$inc": {"views": 1}},  # ✅ Increment views
        return_document=ReturnDocument.AFTER  # ✅ Return the updated document
    )
    if post:
        return post_helper(post)
    else:
        raise HTTPException(status_code=404, detail="Post not found")
    
@router.put("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: str,
    post_update: PostUpdate = Body(...),
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check ownership
    if post.get("author_email") != current_user["email"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    update_data = {k: v for k, v in post_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    update_result = await db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": update_data}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update post")

    updated_post = await db.posts.find_one({"_id": ObjectId(post_id)})
    return post_helper(updated_post)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check ownership
    if post.get("author_email") != current_user["email"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    delete_result = await db.posts.delete_one({"_id": ObjectId(post_id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete post")

    # Return 204 No Content to indicate success with no response body
    return

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    # current_user is dict like {"email": "...", "name": "..."} from token
    post_data = post.model_dump()
    post_data["author_email"] = current_user["email"]
    post_data["author"] = current_user.get("name", "Unknown")
    post_data["date"] = datetime.now(IST)
    post_data["likes"] = []
    post_data["comments"] = []
    post_data["likes_count"] = 0
    post_data["views"] = 0

    result = await db.posts.insert_one(post_data)
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post"
        )

    created_post = await db.posts.find_one({"_id": result.inserted_id})
    return post_helper(created_post)