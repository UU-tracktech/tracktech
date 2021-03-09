import React from 'react';
import { render } from 'react-dom';
import Video from './components/video';
import InputBox from './components/input';
import logo from './logo.svg';
import './App.css';
import './components/video.css';
import './components/input.css';


function App() {
  return (
    <div className="App">
      <header className="App-header">
          <div className="fifty-div">
              <InputBox />
              <Video data-setup='{"fluid": true}'>

              </Video>
          </div>
      </header>
    </div>
  );
}

render(<InputBox />, document.getElementById('root'));

render(<Video />, document.getElementById('root'));



export default App;