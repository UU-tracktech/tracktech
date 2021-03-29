import React from "react"
import ReactAwesomePlayer from 'react-awesome-player'
import './video.css'

class Video extends React.Component { //video player component.
    state = {
        options: {
            poster: "https://cdn.discordapp.com/attachments/809363612404678657/814798379913314304/a.gif",
            sources: [{
                type: "video/mp4",
                src: "https://cdn.theguardian.tv/webM/2015/07/20/150716YesMen_synd_768k_vp8.webm"
            }, {
                type: "application/x-mpegURL",
                src: "http://localhost:50008/hls/movie.m3u8"
            }]
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

export default Video