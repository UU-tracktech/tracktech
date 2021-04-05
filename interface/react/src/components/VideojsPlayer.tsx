import * as React from 'react'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'

export type VideoPlayerProps = { onButtonClick: () => void, onResize?: (width: number, height: number, left: number, top: number) => void } & videojs.PlayerOptions
export class VideoPlayer extends React.Component<VideoPlayerProps> {
    private player?: videojs.Player
    private videoNode?: HTMLVideoElement

    //Offset used for the time based on fragment number
    private offset = 0

    componentDidMount() {
        // instantiate video.js
        this.player = videojs(this.videoNode, this.props, () => {

            var toggleSizeButton = new ToggleSizeButton(this.player, { onClick: this.props.onButtonClick });
            this.player?.controlBar.addChild(toggleSizeButton, { Text: 'Toggle main' }, 0)
            this.player?.on('playerresize', () => this.onResize())
            this.player?.on('play', () => this.onResize())
            this.player?.on('loadeddata', () => this.testFunc())

            //On load, grab metadata and set an offset for our internal timestamp
            //this.player?.on('loadeddata', () => this.GetMetaData())

            //print our internal timestamp to the console for debug info
            this.player?.setInterval(() => this.printTime(), 1000 / 24)
        })
    }

    testFunc() {
        let activeCue = this.player?.textTracks()[0].activeCues;

        if (activeCue)
            if (activeCue[0]) {

                let splitUri = activeCue[0]['value'].uri.split('_V')[1]
                //The extracted number
                let fragNum = splitUri.slice(1, splitUri.length - 3)
                //Set offset based on starttime found in metadata
                let startTime = activeCue[0].startTime
                //each fragment is 2 seconds, so we need fragNum * 2 to get total seconds
                if (startTime == 0) {
                    this.offset = parseFloat(fragNum) * 2
                } else {
                    this.offset = parseFloat(fragNum) * 2 - 2
                }
            }
    }


    /**Gets the metadata track*/
    GetMetaData() {
        let tracks = this.player?.textTracks();
        let segmentMetadataTrack;

        if(tracks) {
            for (let i = 0; i < tracks.length; i++) {
                if (tracks[i].label === 'segment-metadata') {
                    segmentMetadataTrack = tracks[i];
                }
            }

            if (segmentMetadataTrack) {
                segmentMetadataTrack.on('cuechange', this.HandleMetaData(segmentMetadataTrack))
            }
        }
    }

    /**Handles the given metadata and sets an offset
     * to get a correct internal timestamp of the video
     * based on the fragment number*/
    HandleMetaData(segmentMetadataTrack) {
        let activeCue = segmentMetadataTrack.activeCues[0];
        if (activeCue) {
            //The whole filename of the fragment being played
            let splitUri = activeCue['value'].uri.split('_V')[1]
            //The extracted number
            let fragNum = splitUri.slice(1, splitUri.length-3)
            //Set offset based on starttime found in metadata
            let startTime = activeCue.startTime
            //each fragment is 2 seconds, so we need fragNum * 2 to get total seconds
            if(startTime == 0) {
                this.offset = parseFloat(fragNum) * 2
            }
            else {
                this.offset = parseFloat(fragNum) * 2 - 2
            }
        }
    }

    /**Print the internal timestamp to the console as debug info*/
    printTime() {
        if(this.player?.currentTime()) {
            //Get the time with our calculated offset
            let realtime = this.player?.currentTime() + this.offset

            //convert to readable format
            let minutes = Math.floor(realtime / 60)
            let seconds = Math.floor(realtime % 60)
            let playerTime = minutes + ':' + seconds

            console.log('Time', playerTime)
        }
    }

    onResize() {
        if (this.player && this.props.onResize) {
            var player = this.player?.currentDimensions()

            var playerWidth = player.width
            var playerHeight = player.height
            var playerAspect = playerWidth / playerHeight

            var videoWidth = this.player.videoWidth()
            var videoHeight = this.player.videoHeight()
            var videoAspect = videoWidth / videoHeight

            if (playerAspect < videoAspect) {
                var widthRatio = playerWidth / videoWidth
                var actualVideoHeight = widthRatio * videoHeight
                this.props.onResize(playerWidth, actualVideoHeight, 0, (playerHeight - actualVideoHeight) / 2)
            } else {
                var heightRatio = playerHeight / videoHeight
                var actualVideoWidth = heightRatio * videoWidth
                this.props.onResize(actualVideoWidth, playerHeight, (playerWidth - actualVideoWidth) / 2, 0)
            }
        }
    }

    // destroy player on unmount
    componentWillUnmount() {
        this.player?.dispose()
    }

    // wrap the player in a div with a `data-vjs-player` attribute
    // so videojs won't create additional wrapper in the DOM
    // see https://github.com/videojs/video.js/pull/3856
    render() {
        return (
            <div className="c-player" style={{ width: '100%', height: '100%' }}>
                <div className="c-player__screen vjs-fill" data-vjs-player="true" style={{ width: '100%', height: '100%' }}>
                    <video ref={(node: HTMLVideoElement) => this.videoNode = node} className="video-js" />
                </div>
            </div>
        )
    }
}

//https://stackoverflow.com/questions/35604358/videojs-v5-adding-custom-components-in-es6-am-i-doing-it-right
export type ToggleSizeButtonOptions = { onClick: () => void }
class ToggleSizeButton extends videojs.getComponent('Button') {

    private onClick: () => void

    constructor(player, options: ToggleSizeButtonOptions) {
        super(player, {})
        this.controlText('Toggle main')
        this.onClick = options.onClick
        this.addClass('vjs-icon-circle');
    }

    public handleClick(_e) {
        this.onClick()
    }
}