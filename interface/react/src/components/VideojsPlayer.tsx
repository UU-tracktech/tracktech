import * as React from 'react'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'

export type VideoPlayerProps = { onButtonClick: () => void, onResize?: (width: number, height: number, left: number, top: number) => void } & videojs.PlayerOptions
export class VideoPlayer extends React.Component<VideoPlayerProps> {
    private player?: videojs.Player
    private videoNode?: HTMLVideoElement

    //Offset used for the time based on fragment number
    private offset = 0
    private startUri;

    componentDidMount() {
        // instantiate video.js
        this.player = videojs(this.videoNode, this.props, () => {

            var toggleSizeButton = new ToggleSizeButton(this.player, { onClick: this.props.onButtonClick });
            this.player?.controlBar.addChild(toggleSizeButton, { Text: 'Toggle main' }, 0)
            this.player?.on('playerresize', () => this.onResize())
            this.player?.on('play', () => this.onResize())

            this.player?.on('play', () => {
                this.getCurrentTime()
                let uriCheck = this.player?.setInterval(() => {
                    let playerHLS = (this.player?.tech() as any).vhs
                    let media = playerHLS.playlists.media()

                    let currentUri = media.segments[0].uri

                    if (currentUri != this.startUri) {
                        let splitUri = currentUri.split('_V')[1]
                        let fragNum = splitUri.slice(1, splitUri.length - 3)
                        const segmentTimestamp: number = (parseInt(fragNum) - 1) * 2
                        this.offset = segmentTimestamp - 1
                        this.clearInterval(uriCheck)
                        this.player?.currentTime(0)
                        //console.log('Interval done')
                    }
                }, 10)
            })

            this.player?.setInterval(() => {

                let playerTime = this.player?.currentTime();

                if(playerTime) {

                    // console.log('playertime', playerTime)
                    // console.log('offset', this.offset)
                    let stamp = playerTime + this.offset

                    let min = Math.floor(stamp / 60)
                    let sec = Math.floor(stamp % 60)
                    let toPrint = min + ':' + sec

                    console.log('time', toPrint)
                }
            }, 1000/24)
        })
    }

    clearInterval(x) {
        this.player?.clearInterval(x)
    }

    getCurrentTime() {
        let playerHLS = (this.player?.tech() as any).vhs
        //console.log('playerhls', playerHLS)

        let media = playerHLS.playlists.media()
        let lastUri = media.segments[0].uri
        this.startUri = lastUri

        let splitUri = lastUri.split('_V')[1]
        let fragNum = splitUri.slice(1, splitUri.length - 3)
        const segmentTimestamp = (parseInt(fragNum) - 1) * 2
        this.offset = segmentTimestamp

        // let min = Math.floor(segmentTimestamp / 60)
        // let sec = segmentTimestamp % 60
        // let stamp = min + ':' + sec
        //console.log('timestamp', stamp)
        //console.log('currentTime', this.player?.currentTime())
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