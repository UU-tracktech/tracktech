import * as React from 'react'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'

export type VideoPlayerProps = { onClick?: () => void }
export class VideoPlayer extends React.Component<videojs.PlayerOptions & VideoPlayerProps> {
    private player?: videojs.Player
    private videoNode?: HTMLVideoElement

    componentDidMount() {
        // instantiate video.js
        this.player = videojs(this.videoNode, this.props, () => {
            if (this.props.onClick) {
                console.log(this.props.onClick)
                var toggleSizeButton = new ToggleSizeButton(this.player, { onClick: this.props.onClick });
                this.player?.controlBar.addChild(toggleSizeButton, { Text: 'Enlarge' })
            }
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
        this.onClick = options.onClick
        this.addClass('vjs-icon-circle');
    }

    public handleClick(_e) {
        this.onClick()
    }
}