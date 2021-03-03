# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

`npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

`npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

`npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

`npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).


# Setting up ESLint

To set up ESLint for both JavaScript, React and TypeScript:

## Installing ESLint

In WebStorm press `Alt+F12` to open a terminal.

In the terminal run the following commands:

 * `npm install --save-dev eslint` to install ESLint as a development dependency.

 * `npm install eslint-plugin-react --save-dev` to install ESLint for React.

 * `npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin` to install ESLint for TypeScript

## Enabling ESLint in WebStorm

Press `Ctrl+Alt+S` to open Settings/Preferences dialog.

Go to Languages and Framework | JavaScript | Code Quality Tools | ESLint.

Select the Automatic ESLint configuration option.

The ESLint is now enabled for JavaScript, React and TypeScript in the current project.

# Running Docker

## Building React build

First build the build file in WebStorm:

 * Press `Run` -> `Run` or press `Alt+Shift+F10`
 * Select `build` from the options.

### Local testing

For local testing, you could use `npm start` from the run menu. This allows for changes to reflect by simply refreshing
the browser page. This runs React and NodeJS locally.

**BEFORE COMMITTING CODE TO THE GITLAB REPOSITORY, PLEASE TEST IT IN DOCKER INTERFACE. ONLY IF IT ALSO RUNS PROPERLY IN
THE DOCKER ENVIRONMENT SHOULD IT BE PUSHED.**

## Starting Docker

Open PowerShell and build the image.

 * Use `cd "<filepath to dockefile folder>"` to allow PowerShell to find the Dockerfile.

 * Type `docker build -t <image_name> .` in PowerShell.

 * After the building is done, execute to following command: `docker run -p 80:5000 <image_name> serve -s build`.

 * Wait until you see the following: `INFO: Accepting connections at http://localhost:5000`.

 * Afterwards the website can be accessed from `localhost` in your browser.

## Updating the build

### For changes in React build only:

Run the build command in WebStorm as [described before](##Building-React-build).

If previous Docker build is still running: `docker stop <container_name>` in PowerShell. Or press stop on the container
Docker desktop.

 * Use `cd "<filepath to dockefile folder>"` to allow PowerShell to find the Dockerfile.

 * Run `docker build -t <image_name> .` in PowerShell.

 * Run `docker run -p 80:5000 <image_name>` in PowerShell to restart the updated build.

 * Refresh the `localhost` page in your browser.

### For changes in Dockerfile:

Run everything described in [Starting Docker](##Starting-Docker).

Keep in mind that image names should be unique.
