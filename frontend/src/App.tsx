import React from 'react';
import Main from './views/Main';
import ListPatient from './views/ListPatient'
import { BrowserRouter, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/lk" element={<ListPatient />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
