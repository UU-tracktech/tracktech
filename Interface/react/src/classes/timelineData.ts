/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */
/*

This class is used to generate the most interesting events from a long list of tracking
timeline logs.

*/

/** Tracking log type, matching a processor with a timestamp when an object was spotted */
export type trackingLog = { timeStamp: string; processorId: string }
/** Tracking log type, with Date type instead of string */
type datedTrackingLog = { timeStamp: Date; processorId: string }

/** A range from and to a Date */
export type dateRange = { from: Date; to: Date }
/** Dictionary matching camera processor ids to a timeline of events */
export type timelineEvents = { [cameraId: string]: dateRange[] }

/** Object containing a summary of timeline data logs */
export class TimelineData {
  private data: datedTrackingLog[]

  constructor(data: trackingLog[]) {
    this.data = data.map((x) => ({
      timeStamp: ToDate(x.timeStamp),
      processorId: x.processorId
    }))
  }

  /**
   * Create a timeline of important events, which in this case are the moments a camera finds and loses an object
   * @returns The timeline of events for this camera
   */
  GetImportantEvents(): timelineEvents {
    var spottedOn: { [camera: string]: dateRange } = {}
    var events: timelineEvents = {}

    this.data.forEach((logEvent) => {
      // Never seen before
      if (spottedOn[logEvent.processorId] == undefined) {
        spottedOn[logEvent.processorId] = {
          from: logEvent.timeStamp,
          to: logEvent.timeStamp
        }
      }
      // Have seen before
      else {
        var previousRange: dateRange = spottedOn[logEvent.processorId]
        var lastSpotted: Date = previousRange.to
        var trackingThreshold: Date = new Date(
          logEvent.timeStamp.getTime() - 3000
        )
        // Lost sight for a bit
        if (lastSpotted < trackingThreshold) {
          spottedOn[logEvent.processorId] = {
            from: logEvent.timeStamp,
            to: logEvent.timeStamp
          }
          if (events[logEvent.processorId] == undefined) {
            events[logEvent.processorId] = [previousRange]
          } else {
            events[logEvent.processorId].push(previousRange)
          }
        }
        // Did not lose sight for a bit, update to
        else {
          spottedOn[logEvent.processorId].to = logEvent.timeStamp
        }
      }
    })

    // Clean up the last timelines that have not yet been closed
    for (let cameraId in spottedOn) {
      let range: dateRange = spottedOn[cameraId]
      if (events[cameraId] == undefined) {
        events[cameraId] = [range]
      } else {
        events[cameraId].push(range)
      }
    }

    return events
  }
}

/**
 * Convert a string from the server to a date
 * @param logString Logging string from the processor orchestrator
 * @returns
 */
export function ToDate(logString: string): Date {
  var split = logString.split(' | ')
  var ymd = split[0].split('/')
  var hms = split[1].split(':')
  return new Date(
    parseInt(ymd[0]),
    parseInt(ymd[1]),
    parseInt(ymd[2]),
    parseInt(hms[0]),
    parseInt(hms[1]),
    parseInt(hms[2])
  )
}
