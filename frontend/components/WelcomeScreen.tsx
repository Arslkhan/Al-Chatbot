import { MessageSquare, FileText, Scale, Users } from 'lucide-react'

interface WelcomeScreenProps {
  language: 'en' | 'ar'
}

export default function WelcomeScreen({ language }: WelcomeScreenProps) {
  const text = {
    en: {
      welcome: 'Welcome to LegalEdge AI',
      description: 'Your trusted assistant for Dubai real estate and tenancy law',
      features: 'What I can help you with:',
      items: [
        'Dubai tenancy laws and regulations',
        'Landlord and tenant rights',
        'Rental contract terms and conditions',
        'RERA guidelines and procedures',
        'Property disputes and resolutions',
        'When to seek professional legal counsel',
      ],
      cta: 'Ask me anything to get started!',
    },
    ar: {
      welcome: 'مرحبًا بك في LegalEdge AI',
      description: 'مساعدك الموثوق لقانون العقارات والإيجارات في دبي',
      features: 'كيف يمكنني مساعدتك:',
      items: [
        'قوانين ولوائح الإيجار في دبي',
        'حقوق المالك والمستأجر',
        'شروط وأحكام عقد الإيجار',
        'إرشادات وإجراءات ريرا',
        'نزاعات الملكية والحلول',
        'متى يجب طلب استشارة قانونية مهنية',
      ],
      cta: 'اسألني أي شيء للبدء!',
    },
  }

  const icons = [
    <Scale key="scale" className="w-6 h-6" />,
    <Users key="users" className="w-6 h-6" />,
    <FileText key="file" className="w-6 h-6" />,
    <MessageSquare key="message" className="w-6 h-6" />,
    <Scale key="scale2" className="w-6 h-6" />,
    <FileText key="file2" className="w-6 h-6" />,
  ]

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="max-w-xl w-full">
        {/* Icon - Smaller */}
        <div className="flex justify-center mb-4">
          <div className="bg-gradient-to-br from-blue-600 to-blue-700 p-3 rounded-xl shadow-lg">
            <MessageSquare className="w-8 h-8 text-white" />
          </div>
        </div>

        {/* Welcome Text - Smaller */}
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-2">
          {text[language].welcome}
        </h2>
        <p className="text-center text-gray-600 mb-4 text-base">
          {text[language].description}
        </p>

        {/* Features - Compact Grid */}
        <div className="bg-white rounded-xl shadow-md p-4 border border-gray-100 mb-4">
          <h3 className="font-semibold text-gray-900 mb-3 flex items-center space-x-2 rtl:space-x-reverse">
            <FileText className="w-4 h-4 text-blue-600" />
            <span className="text-sm">{text[language].features}</span>
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {text[language].items.map((item, index) => (
              <div key={index} className="flex items-center space-x-2 rtl:space-x-reverse">
                <div className="flex-shrink-0">
                  <div className="bg-blue-100 rounded-md p-1 text-blue-600">
                    {icons[index]}
                  </div>
                </div>
                <span className="text-gray-700 text-sm">{item}</span>
              </div>
            ))}
          </div>
        </div>

        {/* CTA - Smaller */}
        <p className="text-center text-gray-600 text-sm font-medium">
          {text[language].cta}
        </p>
        
        {/* Quick Input Hint - Smaller */}
        <div className="mt-3 text-center">
          <div className="inline-flex items-center px-3 py-1.5 bg-blue-100 text-blue-800 rounded-md text-xs">
            💡 Start typing below to ask your question
          </div>
        </div>
      </div>
    </div>
  )
}

