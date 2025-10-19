import { User, AlertTriangle, CheckCircle, BookOpen } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import FeedbackWidget from './FeedbackWidget'

interface Message {
  id: string
  content: string
  isUser: boolean
  citations?: Citation[]
  confidence?: number
  needsLawyer?: boolean
  timestamp: string
}

interface Citation {
  source: string
  page?: number
  excerpt: string
  relevance_score: number
}

interface MessageBubbleProps {
  message: Message
  language: 'en' | 'ar'
}

export default function MessageBubble({ message, language }: MessageBubbleProps) {
  const text = {
    en: {
      confidence: 'Confidence',
      citations: 'Sources',
      lawyerWarning: 'Consider consulting a licensed lawyer for your specific situation.',
      page: 'Page',
    },
    ar: {
      confidence: 'الثقة',
      citations: 'المصادر',
      lawyerWarning: 'فكر في استشارة محامٍ مرخص لحالتك الخاصة.',
      page: 'صفحة',
    },
  }

  if (message.isUser) {
    return (
      <div className="flex items-start justify-end space-x-3 rtl:space-x-reverse message-animate">
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-2xl px-4 py-3 max-w-2xl shadow-md">
          <p className="whitespace-pre-wrap break-words">{message.content}</p>
        </div>
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
          <User className="w-5 h-5 text-gray-600" />
        </div>
      </div>
    )
  }

  // Assistant message
  const confidenceColor =
    message.confidence && message.confidence >= 0.8
      ? 'text-green-600'
      : message.confidence && message.confidence >= 0.6
      ? 'text-yellow-600'
      : 'text-red-600'

  return (
    <div className="flex items-start space-x-3 rtl:space-x-reverse message-animate">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-600 to-blue-700 flex items-center justify-center">
        <span className="text-white text-xs font-bold">AI</span>
      </div>
      
      <div className="flex-1 max-w-2xl">
        {/* Main message */}
        <div className="bg-white rounded-2xl px-4 py-3 shadow-md border border-gray-100">
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        </div>

        {/* Metadata */}
        {(message.confidence !== undefined || message.needsLawyer || message.citations) && (
          <div className="mt-2 space-y-2">
            {/* Confidence Score */}
            {message.confidence !== undefined && (
              <div className="flex items-center space-x-2 rtl:space-x-reverse text-xs">
                <CheckCircle className={`w-4 h-4 ${confidenceColor}`} />
                <span className="text-gray-600">
                  {text[language].confidence}:{' '}
                  <span className={confidenceColor}>
                    {Math.round(message.confidence * 100)}%
                  </span>
                </span>
              </div>
            )}

            {/* Lawyer Warning */}
            {message.needsLawyer && (
              <div className="bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 flex items-start space-x-2 rtl:space-x-reverse">
                <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                <p className="text-xs text-amber-800">{text[language].lawyerWarning}</p>
              </div>
            )}

            {/* Citations */}
            {message.citations && message.citations.length > 0 && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg px-3 py-2">
                <div className="flex items-center space-x-2 rtl:space-x-reverse mb-2">
                  <BookOpen className="w-4 h-4 text-blue-600" />
                  <span className="text-xs font-medium text-blue-900">
                    {text[language].citations}
                  </span>
                </div>
                <div className="space-y-1">
                  {message.citations.map((citation, index) => (
                    <div key={index} className="text-xs text-blue-800">
                      <span className="font-medium">{citation.source}</span>
                      {citation.page && (
                        <span className="text-blue-600">
                          {' '}
                          ({text[language].page} {citation.page})
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Feedback Widget */}
        <FeedbackWidget messageId={message.id} language={language} />
      </div>
    </div>
  )
}

