'use client'

import { useState } from 'react'
import { ThumbsUp, ThumbsDown, MessageSquare } from 'lucide-react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface FeedbackWidgetProps {
  messageId: string
  language: 'en' | 'ar'
}

export default function FeedbackWidget({ messageId, language }: FeedbackWidgetProps) {
  const [rating, setRating] = useState<number | null>(null)
  const [showComment, setShowComment] = useState(false)
  const [comment, setComment] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const text = {
    en: {
      helpful: 'Was this helpful?',
      comment: 'Tell us more (optional)',
      submit: 'Submit',
      thanks: 'Thank you for your feedback!',
    },
    ar: {
      helpful: 'هل كان هذا مفيدًا؟',
      comment: 'أخبرنا المزيد (اختياري)',
      submit: 'إرسال',
      thanks: 'شكرًا لك على ملاحظاتك!',
    },
  }

  const handleRating = async (value: number) => {
    setRating(value)
    
    if (value >= 4) {
      // Positive rating - submit immediately
      await submitFeedback(value, '')
    } else {
      // Negative rating - ask for comment
      setShowComment(true)
    }
  }

  const submitFeedback = async (ratingValue: number, commentValue: string) => {
    try {
      await axios.post(`${API_URL}/api/feedback`, {
        message_id: messageId,
        rating: ratingValue,
        comment: commentValue || null,
      })
      setSubmitted(true)
    } catch (error) {
      console.error('Error submitting feedback:', error)
    }
  }

  const handleSubmitComment = async () => {
    if (rating) {
      await submitFeedback(rating, comment)
    }
  }

  if (submitted) {
    return (
      <div className="mt-2 text-xs text-green-600 flex items-center space-x-1 rtl:space-x-reverse">
        <MessageSquare className="w-3 h-3" />
        <span>{text[language].thanks}</span>
      </div>
    )
  }

  return (
    <div className="mt-2">
      {!rating ? (
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <span className="text-xs text-gray-600">{text[language].helpful}</span>
          <div className="flex items-center space-x-1 rtl:space-x-reverse">
            <button
              onClick={() => handleRating(5)}
              className="p-1 hover:bg-gray-100 rounded transition-colors"
              title="Yes"
            >
              <ThumbsUp className="w-4 h-4 text-gray-500 hover:text-green-600" />
            </button>
            <button
              onClick={() => handleRating(1)}
              className="p-1 hover:bg-gray-100 rounded transition-colors"
              title="No"
            >
              <ThumbsDown className="w-4 h-4 text-gray-500 hover:text-red-600" />
            </button>
          </div>
        </div>
      ) : showComment && !submitted ? (
        <div className="space-y-2">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder={text[language].comment}
            className="w-full text-xs px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            rows={2}
          />
          <button
            onClick={handleSubmitComment}
            className="text-xs px-3 py-1 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            {text[language].submit}
          </button>
        </div>
      ) : null}
    </div>
  )
}

