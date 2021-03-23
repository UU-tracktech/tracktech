import React from 'react';
import VideoPlayer from "./components/VideojsPlayer";
import './App.css';
import WebSocket from "./components/WebSocket";
import './components/WebSocket.css';

type stream = { name: string, url: string, type: string }
type appState = { streams: stream[] }

class App extends React.Component<{}, appState> {

  constructor(props) {
    super(props);
    this.state = { streams: [] }
  }

  async componentDidMount() {
    var config = await (await fetch(process.env.PUBLIC_URL + '/config.json')).json();
    this.setState({ streams: config.map((stream) => ({
        name: stream.Name, url: stream.Forwarder, type: stream.Type })) })
  }

  render() {
    var sources = this.state.streams.map((stream) => ({
      name: stream.name,
      srcObject: {
        src: stream.url,
        type: stream.type
      }
    }))

    return (
      <div className="App">
        <header className="App-header">
          {
            sources && sources.map((source) =>
              <div>
                <h1>{source.name}</h1>
                <VideoPlayer key={source.name} autoplay={true} controls={true} sources={[source.srcObject]} />
              </div>)
          }
          <div>
            <WebSocket />
          </div>
        </header>
      </div>
    );
  }
}

export default App;