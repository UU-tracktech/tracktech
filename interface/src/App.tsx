import React from 'react';
import { render } from 'react-dom';
import VideoPlayer from "./components/VideojsPlayer";
import logo from './logo.svg';
import './App.css';

const videoJsOptions = {
    autoplay: true,
    controls: true,
    sources: [{
        //src: 'http://vjs.zencdn.net/v/oceans.mp4',
        //type: 'video/mp4',
        src: 'http://sample.vodobox.com/big_buck_bunny_4k/big_buck_bunny_4k.m3u8', //hier uiteindelijk env var.
        type: 'application/x-mpegURL'
    }]
};


function App() {
  return (
    <div className="App">
      <header className="App-header">
          <VideoPlayer {...videoJsOptions} />
      </header>
    </div>
  );
}

console.log("Test: " + process.env.NODE_ENV)
console.log("Environment variable: " + process.env.REACT_APP_TEST) //alle var moeten met REACT_APP_ beginnen

export default App;