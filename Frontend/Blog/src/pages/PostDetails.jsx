import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { formatDate } from '../utils/date';
import PostContent from '../components/PostContent';
import LikeButton from '../components/LikeButton';
import CommentsSection from '../components/CommentsSection';

export default function PostDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);

  const [comments, setComments] = useState([]);
  const [likes, setLikes] = useState(0);
  const [likedByUser, setLikedByUser] = useState(false);


  // Fetch the post details and comments when the component mounts
  useEffect(() => {
    const loggedInUser = JSON.parse(localStorage.getItem('user'));
    setUser(loggedInUser);

    const fetchPost = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/posts/${id}`);
        if (!res.ok) throw new Error('Post not found');
        const data = await res.json();
        setPost(data);
        setComments(data.comments?.reverse() || []);
        setLikes(data.likes_count || 0);
        if (loggedInUser && Array.isArray(data.liked_users)) {
          setLikedByUser(data.liked_users.includes(loggedInUser.email));
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [id]);


  
  if (loading) return <div className="p-6 max-w-4xl mx-auto text-gray-500">Loading post...</div>;
  if (error) return <div className="p-6 max-w-4xl mx-auto text-red-500">{error}</div>;
  if (!post) return <div className="p-6 max-w-4xl mx-auto text-red-500">Post not found.</div>;


  
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <button onClick={() => navigate('/')} className="mb-4 text-sm text-blue-600 hover:underline">
        ← Go Back to Home
      </button>

      <PostContent post={post} likes={likes} />
      <LikeButton
        postId={id}
        user={user}
        likedByUser={likedByUser}
        setLikes={setLikes}
        setLikedByUser={setLikedByUser}
      />
      <CommentsSection
        postId={id}
        user={user}
        comments={comments}
        setComments={setComments}
      />
    </div>
  );
}
