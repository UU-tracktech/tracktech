import * as React from 'react'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'

export type VideoPlayerProps = { onButtonClick: () => void, onResize?: (width: number, height: number, left: number, top: number) => void } & videojs.PlayerOptions
export class VideoPlayer extends React.Component<VideoPlayerProps> {
    private player?: videojs.Player
    private videoNode?: HTMLVideoElement

    componentDidMount() {
        // instantiate video.js
        this.player = videojs(this.videoNode, this.props, () => {

            var toggleSizeButton = new ToggleSizeButton(this.player, { onClick: this.props.onButtonClick });
            this.player?.controlBar.addChild(toggleSizeButton, { Text: 'Toggle main' }, 0)
            this.player?.on('playerresize', () => this.onResize())
            this.player?.on('play', () => this.onResize())
        })
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