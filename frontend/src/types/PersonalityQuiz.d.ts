// src/types/personalityQuiz.d.ts

// PersonalityQuizで使用する質問の型
export interface QuizQuestion {
    question1: string;
    question2: string;
  }
  
  // PersonalityQuizで返される結果の型
  export interface QuizResult {
    name: string;
    personality: string;
    url: string;
  }
  