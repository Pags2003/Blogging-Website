import React from 'react';
import { EyeIcon } from '@heroicons/react/24/solid';
import { Heart } from 'lucide-react';
import { formatDate } from '../utils/date';

export default function Post({ post, likes }) {
  return (
    <>
      <h1 className="text-3xl font-bold mb-4">{post.title || 'Untitled'}</h1>
      <p className="text-sm text-gray-600 mb-1">
        <strong>Author:</strong> {post.author || 'Unknown'} ({post.author_email || 'N/A'})
      </p>
      <p className="text-sm text-gray-500 mb-4">Posted on: {formatDate(post.date)}</p>

      <div className="text-sm text-gray-500 mb-4 flex gap-4">
        <div className="flex items-center gap-1">
          <EyeIcon className="h-4 w-4 text-gray-500" />
          <span>{post.views ?? 0} views</span>
        </div>
        <div className="flex items-center gap-1">
          <Heart className="h-4 w-4 text-gray-500" />
          <span>{likes} likes</span>
        </div>
      </div>

      <p className="text-gray-700 mb-6 whitespace-pre-wrap">{post.content || 'No content available.'}</p>
    </>
  );
}
