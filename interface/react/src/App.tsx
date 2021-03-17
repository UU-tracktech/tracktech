import React from 'react';
import { render } from 'react-dom';
import VideoPlayer from "./components/VideojsPlayer";
import logo from './logo.svg';
import './App.css';
import { Stream } from 'node:stream';
import Canvas1 from './components/CanvasTry'

type stream = { name: string, url: string }
type appState = { streams: stream[] }

class App extends React.Component<{}, appState> {

  constructor(props) {
    super(props);
    this.state = { streams: [] }
  }

  async componentDidMount() {
    var config = await (await fetch(process.env.PUBLIC_URL + '/config.json')).json();
    this.setState({ streams: config.map((stream) => ({ name: stream.Name, url: stream.Forwarder })) })
  }



  render() {
    var sources = this.state.streams.map((stream) => ({
      name: stream.name,
      srcObject: {
        src: stream.url,
        type: 'application/x-mpegURL'
      }
    }))
        //<canvas> </canvas>
    return (
      <div className="App">
        <header className="App-header">
          {
            sources && sources.map((source) =>
              <div>
                <Canvas1></Canvas1>
                <h1>{source.name}</h1>
                  <VideoPlayer key={source.name} autoplay={true} controls={true} sources={[source.srcObject]} />

              </div>)
          }
        </header>
      </div>
    );
  }
}

console.log("test: " + process.env.NODE_ENV)
console.log("Environment variable: " + process.env.REACT_APP_URL) //alle var moeten met REACT_APP_ beginnen

export default App;