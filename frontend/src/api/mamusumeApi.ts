// src/api/umamusumeApi.ts
export interface QuizAnswers {
  question1: string;
  question2: string;
  // 他の質問も追加
}

export interface QuizResult {
  name: string;
  personality: string;
  url: string;
}

export const getUmamusume = async (
  answers: QuizAnswers
): Promise<QuizResult> => {
  const response = await fetch('/api/getUmamusume', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(answers),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch the result');
  }

  const data: QuizResult = await response.json();
  return data;
};
