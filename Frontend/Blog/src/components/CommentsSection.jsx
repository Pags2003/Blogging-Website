import React, { useState } from 'react';
import { formatDate } from '../utils/date';

export default function CommentsSection({ postId, user, comments, setComments }) {
  const [commentText, setCommentText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/posts/${postId}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${user?.token}`,
        },
        body: JSON.stringify({ text: commentText }),
      });

      if (!res.ok) throw new Error('Failed to post comment');
      const newComment = await res.json();
      setComments((prev) => [newComment, ...prev]);
      setCommentText('');
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteComment = async (commentId) => {
    if (!user) return alert('Please log in to delete comments.');
    try {
      const res = await fetch(`http://127.0.0.1:8000/posts/${postId}/comments/${commentId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${user.token}`,
        },
      });

      if (!res.ok) throw new Error('Failed to delete comment');
      setComments((prev) => prev.filter((c) => c.id !== commentId));
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-3">Comments</h2>

      {user ? (
        <form onSubmit={handleCommentSubmit} className="mb-4">
          <textarea
            className="w-full p-2 border border-gray-300 rounded mb-2"
            rows="3"
            placeholder="Write a comment..."
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded"
          >
            {loading ? 'Posting...' : 'Add Comment'}
          </button>
        </form>
      ) : (
        <p className="text-gray-500 mb-4">Log in to write a comment.</p>
      )}

      {comments.length === 0 ? (
        <p className="text-gray-500">No comments yet.</p>
      ) : (
        comments.map((comment) => (
          <div key={comment.id} className="mb-3 border-b border-gray-300 pb-2">
            <p className="text-sm text-gray-600 mb-1 flex justify-between items-center">
              <span>
                <span className="font-bold">{comment.author_name || 'Anonymous'}</span> commented on {formatDate(comment.date)}
              </span>
              {user?.email === comment.author_email && (
                <button
                  onClick={() => handleDeleteComment(comment.id)}
                  className="text-red-500 text-xs hover:underline"
                >
                  Delete
                </button>
              )}
            </p>
            <p>{comment.text}</p>
          </div>
        ))
      )}
    </div>
  );
}
