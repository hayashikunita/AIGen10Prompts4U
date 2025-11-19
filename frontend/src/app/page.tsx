'use client';

import { useState, useEffect, useRef } from 'react';
import { getCategories, getPrompts, sendChatMessage, uploadFile, getChatHistories, saveChatHistory, deleteChatHistory, getChatHistory } from '@/lib/api';
import type { Category, Prompt, Message, ChatHistory, UploadedFile } from '@/lib/api';
import ReactMarkdown from 'react-markdown';

export default function Home() {
  // モード管理: 'prompt-display' | 'chatbot'
  const [mode, setMode] = useState<'prompt-display' | 'chatbot'>('chatbot');
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [selectedPrompt, setSelectedPrompt] = useState<Prompt | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [chatHistories, setChatHistories] = useState<ChatHistory[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [showPromptSelector, setShowPromptSelector] = useState(false);
  const [generatedPrompts, setGeneratedPrompts] = useState<Prompt[]>([]);
  const [promptCount, setPromptCount] = useState(10);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    loadCategories();
    loadChatHistories();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const loadPrompts = async (category: string) => {
    try {
      const data = await getPrompts(category);
      setPrompts(data.prompts);
    } catch (error) {
      console.error('Failed to load prompts:', error);
    }
  };

  const loadChatHistories = async () => {
    try {
      const data = await getChatHistories();
      setChatHistories(data);
    } catch (error) {
      console.error('Failed to load chat histories:', error);
    }
  };

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
    loadPrompts(category);
  };

  const handlePromptSelect = (prompt: Prompt) => {
    if (messages.length > 0) {
      const title = `会話_${new Date().toISOString().replace(/[:.]/g, '-')}`;
      saveChatHistory(title, messages, selectedPrompt || undefined).catch(console.error);
    }
    
    setSelectedPrompt(prompt);
    setMessages([]);
    setUploadedFiles([]);
    setShowPromptSelector(false);
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files) return;

    for (const file of Array.from(files)) {
      try {
        const uploaded = await uploadFile(file);
        setUploadedFiles(prev => [...prev, uploaded]);
      } catch (error) {
        console.error('Failed to upload file:', error);
        alert(`ファイルのアップロードに失敗しました: ${file.name}`);
      }
    }

    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim() && uploadedFiles.length === 0) return;
    if (isLoading) return;

    let messageContent = input;

    if (uploadedFiles.length > 0) {
      const fileContents = uploadedFiles.map(file => {
        const icon = { pdf: '📕', word: '📘', excel: '📊', csv: '📄', text: '📝' }[file.file_type] || '📄';
        const truncateWarning = file.truncated ? ' ⚠️ (ファイルが大きいため一部省略されました)' : '';
        return `\n\n--- ${icon} ${file.filename}${truncateWarning} ---\n${file.content}`;
      }).join('');
      
      messageContent += fileContents;
    }

    const userMessage: Message = { role: 'user', content: messageContent };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setUploadedFiles([]);
    setIsLoading(true);

    try {
      let assistantContent = '';
      const assistantMessage: Message = { role: 'assistant', content: '' };
      setMessages(prev => [...prev, assistantMessage]);

      await sendChatMessage(
        newMessages,  // 修正: 新しいメッセージ配列を使用
        selectedPrompt?.system_prompt,
        (chunk) => {
          assistantContent += chunk;
          setMessages(prev => {
            const newMessages = [...prev];
            newMessages[newMessages.length - 1] = { role: 'assistant', content: assistantContent };
            return newMessages;
          });
        }
      );
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = { 
          role: 'assistant', 
          content: `❌ エラーが発生しました: ${error instanceof Error ? error.message : '不明なエラー'}` 
        };
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    if (messages.length > 0) {
      const title = `会話_${new Date().toISOString().replace(/[:.]/g, '-')}`;
      saveChatHistory(title, messages, selectedPrompt || undefined)
        .then(() => {
          loadChatHistories();
          alert('✅ 前の会話を自動保存しました');
        })
        .catch(console.error);
    }
    
    setMessages([]);
    setUploadedFiles([]);
  };

  const handleSaveChat = () => {
    if (messages.length === 0) return;
    
    const title = prompt('会話のタイトルを入力してください:', `会話_${new Date().toISOString().replace(/[:.]/g, '-')}`);
    if (!title) return;

    saveChatHistory(title, messages, selectedPrompt || undefined)
      .then(() => {
        loadChatHistories();
        alert('✅ 会話を保存しました');
      })
      .catch(error => {
        console.error('Failed to save chat:', error);
        alert('❌ 保存に失敗しました');
      });
  };

  const handleLoadHistory = async (filename: string) => {
    try {
      const history = await getChatHistory(filename);
      setMessages(history.messages);
      setSelectedPrompt(history.selected_prompt);
      setShowHistory(false);
    } catch (error) {
      console.error('Failed to load history:', error);
      alert('❌ 履歴の読み込みに失敗しました');
    }
  };

  const handleDeleteHistory = async (filename: string) => {
    if (!confirm('この履歴を削除しますか？')) return;

    try {
      await deleteChatHistory(filename);
      loadChatHistories();
      alert('✅ 履歴を削除しました');
    } catch (error) {
      console.error('Failed to delete history:', error);
      alert('❌ 削除に失敗しました');
    }
  };

  const handleGeneratePrompts = async () => {
    if (!selectedCategory) {
      alert('カテゴリを選択してください');
      return;
    }

    try {
      const data = await getPrompts(selectedCategory);
      setGeneratedPrompts(data.prompts);
    } catch (error) {
      console.error('Failed to generate prompts:', error);
      alert('❌ プロンプトの生成に失敗しました');
    }
  };

  const handleCopyPrompt = (prompt: Prompt) => {
    const text = `タイトル: ${prompt.title}\n\nシステムプロンプト:\n${prompt.system_prompt}\n\n推奨添付ファイル:\n${prompt.recommended_attachments.join(', ')}`;
    navigator.clipboard.writeText(text);
    alert('📋 プロンプトをコピーしました');
  };

  const handleUseChatWithPrompt = (prompt: Prompt) => {
    setSelectedPrompt(prompt);
    setMode('chatbot');
    setMessages([]);
    setUploadedFiles([]);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* サイドバー */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
            AIGenPrompts4U
          </h1>
          <p className="text-sm text-gray-500 mt-1">GPT-5 搭載</p>
        </div>

        {/* モード切替ナビゲーション */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex gap-2">
            <button
              onClick={() => setMode('prompt-display')}
              className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                mode === 'prompt-display'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              🎲 プロンプト表示
            </button>
            <button
              onClick={() => setMode('chatbot')}
              className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                mode === 'chatbot'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              💬 チャットボット
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          <div className="mb-6">
            <button
              onClick={() => setShowPromptSelector(!showPromptSelector)}
              className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              📋 プロンプトを選択
            </button>

            {showPromptSelector && (
              <div className="mt-4 space-y-3">
                <select
                  value={selectedCategory}
                  onChange={(e) => handleCategoryChange(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white text-gray-900"
                >
                  <option value="">カテゴリを選択</option>
                  {categories.map((cat) => (
                    <option key={cat.key} value={cat.key}>
                      {cat.name}
                    </option>
                  ))}
                </select>

                {prompts.length > 0 && (
                  <div className="max-h-96 overflow-y-auto space-y-2">
                    {prompts.map((prompt) => (
                      <button
                        key={prompt.id}
                        onClick={() => handlePromptSelect(prompt)}
                        className="w-full text-left px-3 py-2 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm text-gray-900 transition-colors"
                      >
                        {prompt.title}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          {selectedPrompt && (
            <div className="mb-6 p-3 bg-purple-50 rounded-lg">
              <p className="text-xs text-purple-600 font-semibold mb-1">選択中のプロンプト</p>
              <p className="text-sm text-gray-800">{selectedPrompt.title}</p>
            </div>
          )}

          <div>
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              📚 履歴 ({chatHistories.length})
            </button>

            {showHistory && (
              <div className="mt-4 space-y-2 max-h-96 overflow-y-auto">
                {chatHistories.map((history) => (
                  <div key={history.filename} className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <button
                        onClick={() => handleLoadHistory(history.filename)}
                        className="text-sm font-medium text-gray-800 hover:text-purple-600 text-left flex-1"
                      >
                        {history.title}
                      </button>
                      <button
                        onClick={() => handleDeleteHistory(history.filename)}
                        className="text-red-500 hover:text-red-700 ml-2"
                      >
                        🗑️
                      </button>
                    </div>
                    <p className="text-xs text-gray-500">
                      {history.message_count}メッセージ • {history.timestamp}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="p-4 border-t border-gray-200 space-y-2">
          {mode === 'chatbot' && (
            <>
              <button
                onClick={handleNewChat}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                🆕 新しい会話
              </button>
              <button
                onClick={handleSaveChat}
                disabled={messages.length === 0}
                className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                💾 会話を保存
              </button>
            </>
          )}
          {mode === 'prompt-display' && (
            <button
              onClick={handleGeneratePrompts}
              disabled={!selectedCategory}
              className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              🎲 プロンプト生成
            </button>
          )}
        </div>
      </div>

      {/* メインエリア */}
      <div className="flex-1 flex flex-col">
        {mode === 'chatbot' ? (
          // チャットボットモード
          <>
            <div className="flex-1 overflow-y-auto p-6">
              {messages.length === 0 ? (
                <div className="h-full flex items-center justify-center">
                  <div className="text-center max-w-2xl">
                    <h2 className="text-3xl font-bold text-gray-800 mb-4">💬 チャットを開始</h2>
                    <p className="text-gray-600 mb-6">
                      左のサイドバーから<strong>「プロンプトを選択」</strong>でシステムプロンプトを設定できます
                      <br />
                      ファイルを添付して、AIに分析させることもできます
                    </p>
                    <div className="flex gap-3 justify-center flex-wrap">
                      <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm">📕 PDF対応</span>
                      <span className="px-4 py-2 bg-orange-100 text-orange-700 rounded-full text-sm">📊 Excel対応</span>
                      <span className="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm">📝 コード対応</span>
                      <span className="px-4 py-2 bg-cyan-100 text-cyan-700 rounded-full text-sm">🤖 GPT-5搭載</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-4 max-w-4xl mx-auto">
                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-3xl rounded-2xl px-4 py-3 ${
                          message.role === 'user'
                            ? 'bg-blue-600 text-white'
                            : 'bg-white text-gray-800 border border-gray-200'
                        }`}
                    >
                      <div className="prose prose-sm max-w-none">
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          <div className="border-t border-gray-200 bg-white p-4">
            <div className="max-w-4xl mx-auto">
              {uploadedFiles.length > 0 && (
                <div className="mb-3 flex gap-2 flex-wrap">
                  {uploadedFiles.map((file, index) => (
                    <div key={index} className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg text-sm">
                      <span>
                        {{ pdf: '📕', word: '📘', excel: '📊', csv: '📄', text: '📝' }[file.file_type] || '📄'}
                      </span>
                      <span className="text-gray-700">{file.filename}</span>
                      {file.truncated && <span className="text-orange-600">⚠️</span>}
                      <button
                        onClick={() => setUploadedFiles(prev => prev.filter((_, i) => i !== index))}
                        className="ml-2 text-red-500 hover:text-red-700"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex gap-3">
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  onChange={handleFileUpload}
                  className="hidden"
                  accept=".pdf,.docx,.xlsx,.xls,.csv,.txt,.py,.js,.ts,.tsx,.jsx,.json,.md"
                />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                  title="ファイルを添付"
                >
                  📎
                </button>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="メッセージを入力してください..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white text-gray-900 placeholder-gray-500"
                  disabled={isLoading}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isLoading || (!input.trim() && uploadedFiles.length === 0)}
                  className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  {isLoading ? '送信中...' : '送信'}
                </button>
              </div>
            </div>
          </div>
        </>
        ) : (
          // プロンプト表示モード
          <div className="flex-1 overflow-y-auto p-6">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-3xl font-bold text-gray-800 mb-6">🎲 プロンプト表示モード</h2>
              
              {generatedPrompts.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-gray-600 mb-4">
                    左のサイドバーからカテゴリを選択し、「🎲 プロンプト生成」ボタンをクリックしてください
                  </p>
                  <div className="flex gap-3 justify-center flex-wrap">
                    <span className="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm">28カテゴリ</span>
                    <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm">1,120プロンプト</span>
                    <span className="px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm">GPT-5対応</span>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
                    <p className="text-sm text-purple-800">
                      <strong>{generatedPrompts.length}個</strong>のプロンプトを生成しました
                      {selectedCategory && <span> (カテゴリ: <strong>{categories.find(c => c.key === selectedCategory)?.name}</strong>)</span>}
                    </p>
                  </div>

                  {generatedPrompts.map((prompt, index) => (
                    <div key={prompt.id} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
                      <div className="flex justify-between items-start mb-4">
                        <h3 className="text-xl font-bold text-gray-800">
                          {index + 1}. {prompt.title}
                        </h3>
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleCopyPrompt(prompt)}
                            className="px-3 py-1 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm"
                          >
                            📋 コピー
                          </button>
                          <button
                            onClick={() => handleUseChatWithPrompt(prompt)}
                            className="px-3 py-1 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm"
                          >
                            💬 チャット開始
                          </button>
                        </div>
                      </div>

                      <div className="mb-4">
                        <h4 className="text-sm font-semibold text-gray-600 mb-2">システムプロンプト:</h4>
                        <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-800 whitespace-pre-wrap border border-gray-200">
                          {prompt.system_prompt}
                        </div>
                      </div>

                      <div>
                        <h4 className="text-sm font-semibold text-gray-600 mb-2">推奨添付ファイル:</h4>
                        <div className="flex gap-2 flex-wrap">
                          {prompt.recommended_attachments.map((attachment, i) => (
                            <span
                              key={i}
                              className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs"
                            >
                              {attachment}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
