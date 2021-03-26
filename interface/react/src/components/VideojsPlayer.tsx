import * as React from 'react'
import videojs from 'video.js'

// Styles
import 'video.js/dist/video-js.css'

class VideoPlayer extends React.Component<videojs.PlayerOptions> {
    private player?: videojs.Player
    private videoNode?: HTMLVideoElement

    componentDidMount() {
        // instantiate video.js
        this.player = videojs(this.videoNode, this.props).ready(function () {
            //console.log('onPlayerReady')
        })
    }


    // destroy player on unmount
    componentWillUnmount() {
        this.player?.dispose()
    }

    // wrap the player in a div with a `data-vjs-player` attribute
    // so videojs won't create additional wrapper in the DOM
    // see https://github.com/videojs/video.js/pull/3856
    render() {
        console.log("render")
        return (
            <div className="c-player">
                <div className="c-player__screen" data-vjs-player="true">
                    <video ref={(node: HTMLVideoElement) => this.videoNode = node} className="video-js" />
                </div>
                {}                {/*<div className="c-player__controls">
                    <button>Play</button>
                    <button>Pause</button>
                </div>*/}
            </div>
        )
    }
}

export default VideoPlayer