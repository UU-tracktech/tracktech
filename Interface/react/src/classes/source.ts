/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

/**
 * Defines the properties of a single camera feed.
 * Contains an identifier, a name, and the stream URL.
 */
export type stream = {
  id: string
  name: string
  srcObject: source
}

/** Defines the properties of a single stream URL. */
export type source = { src: string; type: string }
