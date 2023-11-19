import './App.css';
import { useState } from 'react';
import { createContext } from 'react';
import Login from './components/Login';
import Notes from './components/Notes';
export const UserContext= createContext(null);
function App() {
  const [user, setUsers] = useState(window.sessionStorage.getItem('user') || null);


  return (
    <div className="App">
      <UserContext.Provider value={{user:user, setUser:setUsers}}>
      {user ? (

        <Notes />
      ) : (

        <Login/>
      )}
      </UserContext.Provider>
    </div>
  );
}

export default App;
