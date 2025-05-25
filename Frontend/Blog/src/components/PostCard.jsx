import React from "react";
import { Link } from "react-router-dom";

export default function PostCard({ post }) {
  return (
    <div
      key={post.id}
      className="bg-white rounded-xl shadow-md p-5 mb-4 border border-gray-100 hover:shadow-lg transition"
    >
      <h2 className="text-xl font-semibold mb-2">{post.title}</h2>
      <p className="text-gray-700 mb-2">{post.content.slice(0, 100)}...</p>
      <p className="text-sm text-gray-500 mb-2">
        By <span className="font-semibold">{post.author}</span> on {new Date(post.date).toLocaleDateString("en-GB")}
      </p>
      <Link to={`/posts/${post.id}`} className="text-blue-600 hover:underline text-sm">
        Read More
      </Link>
    </div>
  );
}
