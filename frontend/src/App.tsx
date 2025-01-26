import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import PersonalityQuiz from './components/PersonalityQuiz';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginForm />} /> {/* ログイン画面 */}
        <Route path="/quiz" element={<PersonalityQuiz />} />{' '}
        {/* 性格診断画面 */}
      </Routes>
    </Router>
  );
};

export default App;
