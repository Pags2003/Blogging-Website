import React from "react";
import PostCard from "./PostCard";

export default function PostsList({ loading, posts }) {
  if (loading) {
    return <p className="text-gray-500">Loading posts...</p>;
  }

  if (posts.length === 0) {
    return <p className="text-gray-500">No posts found.</p>;
  }

  return (
    <>
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </>
  );
}
