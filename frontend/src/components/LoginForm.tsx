import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';  // 画面遷移用

const PersonalityQuiz: React.FC = () => {
  const [question1, setQuestion1] = useState('');
  const [question2, setQuestion2] = useState('');
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();  // 画面遷移を行うためのフック

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const token = localStorage.getItem('token');  // 保存したトークンを取得

    if (!token) {
      setError('No token found. Please login first.');
      navigate('/');  // トークンがない場合はログイン画面にリダイレクト
      return;
    }

    setIsLoading(true);  // ローディング開始
    setError('');  // エラーメッセージをクリア

    try {
      console.log("Sending request with data:");
      console.log("Question 1:", question1);
      console.log("Question 2:", question2);

      const response = await fetch(`${process.env.REACT_APP_API_URL}/getUmamusume`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,  // トークンをヘッダーに含める
        },
        body: JSON.stringify({
          question1: question1,
          question2: question2,
        }),
      });

      console.log("Response status:", response.status);

      if (response.status === 401) {
        // トークンの期限切れや認証エラーが発生した場合
        setError('Session expired. Please login again.');
        localStorage.removeItem('token');  // トークンを削除
        navigate('/');  // ログイン画面にリダイレクト
        return;
      }

      if (!response.ok) {
        const errorResponse = await response.json();
        console.error("Error response from server:", errorResponse);
        throw new Error(errorResponse.detail || 'Failed to fetch data');
      }

      const data = await response.json();
      console.log("Received result:", data);
      setResult(data);
    } catch (err: any) {
      console.error("Error occurred:", err);
      setError(err.message || 'Failed to get the result. Please try again.');
    } finally {
      setIsLoading(false);  // ローディング解除
    }
  };

  return (
    <div>
      <h2>Personality Quiz</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Question 1:
            <input
              type="text"
              value={question1}
              onChange={(e) => setQuestion1(e.target.value)}
            />
          </label>
        </div>
        <div>
          <label>
            Question 2:
            <input
              type="text"
              value={question2}
              onChange={(e) => setQuestion2(e.target.value)}
            />
          </label>
        </div>
        <button type="submit" disabled={isLoading}>Submit</button>
      </form>

      {/* ローディング中に表示されるコンポーネント */}
      {isLoading && <p>Loading... Please wait.</p>}
      
      {/* エラーメッセージの表示 */}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {/* 結果の表示 */}
      {result && (
        <div>
          <h3>Recommended Umamusume:</h3>
          <p>Name: {result.name}</p>
          <p>Personality: {result.personality}</p>
          <p>
            <a href={result.url} target="_blank" rel="noopener noreferrer">
              Official Profile
            </a>
          </p>
        </div>
      )}
    </div>
  );
};

export default PersonalityQuiz;
