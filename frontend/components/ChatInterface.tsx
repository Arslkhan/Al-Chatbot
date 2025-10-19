'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Loader2 } from 'lucide-react'
import axios from 'axios'
import MessageBubble from './MessageBubble'

const API_URL = process.env.NEXT_PUBLIC_API_URL || (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8000')

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

interface ChatInterfaceProps {
  conversationId: string | null
  onConversationStart: (id: string) => void
  language: 'en' | 'ar'
  onMessageSent: () => void
}

export default function ChatInterface({
  conversationId,
  onConversationStart,
  language,
  onMessageSent,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const text = {
    en: {
      placeholder: '💬 Ask a legal question about Dubai real estate...',
      send: 'Send',
      typing: 'LegalEdge AI is typing...',
    },
    ar: {
      placeholder: '💬 اسأل سؤالاً قانونيًا حول العقارات في دبي...',
      send: 'إرسال',
      typing: 'LegalEdge AI يكتب...',
    },
  }

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'
    }
  }, [input])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      isUser: true,
      timestamp: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    onMessageSent()

    try {
      const response = await axios.post(`${API_URL}/ask`, {
        question: input,
        language: language,
        jurisdictionCode: "DXB",
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.data.answer,
        isUser: false,
        citations: response.data.citations,
        confidence: response.data.confidence === "High" ? 0.9 : response.data.confidence === "Medium" ? 0.7 : 0.5,
        needsLawyer: response.data.confidence === "Low",
        timestamp: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, assistantMessage])

      if (!conversationId) {
        // Generate a conversation ID for the new API
        onConversationStart(Date.now().toString())
      }
    } catch (error) {
      console.error('Error sending message:', error)
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: language === 'en' 
          ? 'Sorry, there was an error processing your request. Please make sure the backend is running and try again.'
          : 'عذرًا، حدث خطأ في معالجة طلبك. يرجى التأكد من تشغيل الخادم والمحاولة مرة أخرى.',
        isUser: false,
        timestamp: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex-1 flex flex-col min-h-0">
      {/* Messages Area - Scrollable */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden px-6 py-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-8">
            {language === 'en' ? 'Start a conversation...' : 'ابدأ محادثة...'}
          </div>
        )}
        
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} language={language} />
        ))}
        
        {/* Typing Indicator */}
        {isLoading && (
          <div className="flex items-start space-x-3 rtl:space-x-reverse message-animate">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-600 to-blue-700 flex items-center justify-center">
              <span className="text-white text-xs font-bold">AI</span>
            </div>
            <div className="bg-white rounded-2xl px-4 py-3 shadow-md border border-gray-100">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-600 rounded-full typing-dot"></div>
                <div className="w-2 h-2 bg-blue-600 rounded-full typing-dot"></div>
                <div className="w-2 h-2 bg-blue-600 rounded-full typing-dot"></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4 flex-shrink-0">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-end space-x-3 rtl:space-x-reverse">
            <div className="flex-1 relative">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={text[language].placeholder}
                className="w-full px-4 py-3 pr-12 rtl:pr-4 rtl:pl-12 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none max-h-32 shadow-sm"
                rows={1}
                disabled={isLoading}
              />
              <div className="absolute bottom-3 right-3 rtl:right-auto rtl:left-3 text-xs text-gray-400">
                {input.length} / 2000
              </div>
            </div>
            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="flex-shrink-0 bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center space-x-2 rtl:space-x-reverse"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span className="hidden sm:inline">{text[language].send}</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

