import React, { useState } from 'react';
import { Heart, HeartOff } from 'lucide-react';

export default function LikeButton({ postId, user, likedByUser, setLikes, setLikedByUser }) {
  const [loading, setLoading] = useState(false);

  const handleLikeToggle = async () => {
    if (!user) return alert('Please log in to like posts.');

    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/posts/${postId}/like`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${user.token}`,
        },
      });

      if (!res.ok) throw new Error('Failed to toggle like');
      const data = await res.json();
      setLikes(data.likes_count);
      setLikedByUser(data.liked);
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleLikeToggle}
      disabled={loading}
      className={`mb-6 px-4 py-2 rounded flex items-center gap-2 ${
        likedByUser ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
      }`}
    >
      {likedByUser ? <Heart fill="white" size={18} /> : <HeartOff size={18} />}
      {likedByUser ? 'Liked' : 'Like'} 
    </button>
  );
}
