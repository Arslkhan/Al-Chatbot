import { Scale, Trash2, Globe } from 'lucide-react'

interface HeaderProps {
  language: 'en' | 'ar'
  onLanguageChange: (lang: 'en' | 'ar') => void
  onClearChat: () => void
}

export default function Header({ language, onLanguageChange, onClearChat }: HeaderProps) {
  const text = {
    en: {
      title: 'LegalEdge AI',
      subtitle: 'Dubai Real Estate Legal Assistant',
      clear: 'Clear Chat',
    },
    ar: {
      title: 'LegalEdge AI',
      subtitle: 'مساعد قانوني للعقارات في دبي',
      clear: 'مسح المحادثة',
    },
  }

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="px-6 py-4 flex items-center justify-between">
        {/* Logo and Title */}
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <div className="bg-gradient-to-br from-blue-600 to-blue-700 p-2 rounded-xl shadow-lg">
            <Scale className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">{text[language].title}</h1>
            <p className="text-sm text-gray-600">{text[language].subtitle}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          {/* Language Toggle */}
          <button
            onClick={() => onLanguageChange(language === 'en' ? 'ar' : 'en')}
            className="flex items-center space-x-2 rtl:space-x-reverse px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
            title="Toggle Language"
          >
            <Globe className="w-4 h-4" />
            <span className="text-sm font-medium">{language === 'en' ? 'العربية' : 'English'}</span>
          </button>

          {/* Clear Chat */}
          <button
            onClick={onClearChat}
            className="flex items-center space-x-2 rtl:space-x-reverse px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg transition-colors"
            title={text[language].clear}
          >
            <Trash2 className="w-4 h-4" />
            <span className="text-sm font-medium hidden md:inline">{text[language].clear}</span>
          </button>
        </div>
      </div>
    </header>
  )
}

