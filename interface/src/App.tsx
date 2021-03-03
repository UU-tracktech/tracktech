import React from 'react';
import { render } from 'react-dom';
import ReactAwesomePlayer from 'react-awesome-player';
import logo from './logo.svg';
import './App.css';


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <Video>

      </Video>
    </div>
  );
}

class Video extends React.Component { //video player component.
  state = {
    options: {
      poster: "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=854361313,3188166359&fm=26&gp=0.jpg",
      sources: [{
        //type: "video/mp4",
        //src: "https://cdn.theguardian.tv/webM/2015/07/20/150716YesMen_synd_768k_vp8.webm"
        type: "application/x-mpegURL",
        src: "http://d3rlna7iyyu8wu.cloudfront.net/skip_armstrong/skip_armstrong_multichannel_subs.m3u8"
      }],
      subtitles: [{
        language: 'zh',
        url: "https://feawesome.github.io/react-awesome-player/zh.vtt",
        label: "中文"
      },
        {
          language: 'en',
          url: "https://feawesome.github.io/react-awesome-player/en.vtt",
          label: "EN"
        }],
      defaultSubtitle: 'en'
    }
  }
  loadeddata() {
    console.log('loadeddata')
  }
  canplay() {
    console.log('canplay')
  }
  canplaythrough() {
    console.log('canplaythrough')
  }
  play() {
    console.log('play')
  }
  pause() {
    console.log('pause')
  }
  waiting() {
    console.log('waiting')
  }
  playing() {
    console.log('playing')
  }
  ended() {
    console.log('ended')
  }
  error() {
    console.log('error')
  }

  render () {
    const { options } = this.state
    return <div className="video-player">
      <ReactAwesomePlayer
          onRef={video => { console.log(video) }}
          options={options}
          loadeddata={this.loadeddata}
          canplay={this.canplay}
          canplaythrough={this.canplaythrough}
          play={this.play}
          pause={this.pause}
          waiting={this.waiting}
          playing={this.playing}
          ended={this.ended}
          error={this.error}
      />
    </div>
  }
}

render(<Video />, document.getElementById('root'));

export default App;