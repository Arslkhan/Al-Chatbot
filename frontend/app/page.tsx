'use client'

import React, { useState, useEffect } from 'react'
import ChatInterface from '@/components/ChatInterface'
import Header from '@/components/Header'
import Disclaimer from '@/components/Disclaimer'
import WelcomeScreen from '@/components/WelcomeScreen'

export default function Home() {
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [language, setLanguage] = useState<'en' | 'ar'>('en')
  const [hasMessages, setHasMessages] = useState(false)

  return (
    <div className={`min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100 ${language === 'ar' ? 'rtl font-arabic' : ''}`}>
      <div className="max-w-7xl mx-auto h-screen flex flex-col">
        {/* Header */}
        <Header 
          language={language} 
          onLanguageChange={setLanguage}
          onClearChat={() => {
            setConversationId(null)
            setHasMessages(false)
          }}
        />

        {/* Disclaimer */}
        <Disclaimer language={language} />

        {/* Main Content */}
        <div className="flex-1 flex flex-col min-h-0">
          {!hasMessages && (
            <div className="flex-shrink-0">
              <WelcomeScreen language={language} />
            </div>
          )}
          
          <div className="flex-1 flex flex-col min-h-0">
            <ChatInterface 
              conversationId={conversationId}
              onConversationStart={setConversationId}
              language={language}
              onMessageSent={() => setHasMessages(true)}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

