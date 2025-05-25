import React, { useState, useEffect } from 'react';
import SearchBar from '../components/SearchBar';
import PostsList from '../components/PostsList';

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  
  const fetchPosts = async (query = "") => {
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/posts/?search=${encodeURIComponent(query)}`);
      const data = await response.json();
      setPosts(data);
    } catch (error) {
      console.error("Error fetching posts:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      fetchPosts(search);
    }, 300);

    return () => clearTimeout(delayDebounce);
  }, [search]);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">📰 Blog Posts</h1>
      <SearchBar search={search} setSearch={setSearch} />
      <PostsList loading={loading} posts={posts} />
    </div>
  );
}
