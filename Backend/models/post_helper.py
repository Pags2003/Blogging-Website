def post_helper(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post.get("title"),
        "content": post.get("content"),
        "author": post.get("author"),
        "author_email": post.get("author_email"),
        "date": post.get("date").strftime("%Y-%m-%dT%H:%M:%S") if post.get("date") else None,
        "comments": post.get("comments", []),
        "likes_count": len(post.get("likes", [])),
        "liked_users": post.get("likes", []),
        "views": post.get("views", 0) 
    }
