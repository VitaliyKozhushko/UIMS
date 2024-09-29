import React from 'react';
import Main from './views/Main';
import ListPatient from './views/ListPatient'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store';
import ProtectedRoute from './components/ProtectedRoute'
import PersonalAccount from './views/PersonalAccount'

function App() {
  return (
    <BrowserRouter>
      <Provider store={store}>
        <div className="App">
          <Routes>
            <Route path="/" element={<Main/>}/>
            <Route
              path='/lk'
              element={
                <ProtectedRoute>
                  <PersonalAccount/>
                </ProtectedRoute>
              }>
              <Route path="/lk" element={<ListPatient/>}/>
            </Route>
          </Routes>
        </div>
      </Provider>
    </BrowserRouter>
  );
}

export default App;
