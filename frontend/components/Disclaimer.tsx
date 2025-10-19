'use client'

import React, { useState } from 'react'
import { AlertCircle, X } from 'lucide-react'

interface DisclaimerProps {
  language: 'en' | 'ar'
}

export default function Disclaimer({ language }: DisclaimerProps) {
  const [isVisible, setIsVisible] = useState(true)

  const text = {
    en: {
      title: 'Important Disclaimer:',
      message: 'This chatbot provides general legal information only about Dubai real estate and tenancy law. It is not a substitute for professional legal advice. Please consult a licensed lawyer for advice specific to your situation.',
    },
    ar: {
      title: 'إخلاء مسؤولية مهم:',
      message: 'يوفر هذا الروبوت معلومات قانونية عامة فقط حول قانون العقارات والإيجارات في دبي. إنه ليس بديلاً عن المشورة القانونية المهنية. يرجى استشارة محامٍ مرخص للحصول على مشورة خاصة بحالتك.',
    },
  }

  if (!isVisible) return null

  return (
    <div className="mx-6 mt-4 bg-amber-50 border border-amber-200 rounded-lg p-4 relative">
      <button
        onClick={() => setIsVisible(false)}
        className="absolute top-3 right-3 rtl:right-auto rtl:left-3 text-amber-600 hover:text-amber-800 transition-colors"
        aria-label="Close disclaimer"
      >
        <X className="w-5 h-5" />
      </button>
      
      <div className="flex items-start space-x-3 rtl:space-x-reverse pr-8 rtl:pr-0 rtl:pl-8">
        <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
        <div>
          <h3 className="font-semibold text-amber-900 text-sm">
            {text[language].title}
          </h3>
          <p className="text-amber-800 text-sm mt-1">
            {text[language].message}
          </p>
        </div>
      </div>
    </div>
  )
}

