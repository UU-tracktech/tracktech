## Running the pipeline:

* Navigate to the Run Pipeline page or <a href="https://git.science.uu.nl/e.w.j.bangma/tracktech/-/pipelines/new" target="_blank">Click Here</a>.
* Select desired branch.
* Input the variables of the desired pipeline
* Use comma separated Input variable values to run multiple at the same time e.g. `project` value: `processor, orchestrator`

| Input variable key   | Input variable value     | Description									                                            |
|:---------------------|:-------------------------|:----------------------------------------------------------------------------------------|
| `CI_PIPELINE_SOURCE` | `merge_request_event`    | Runs the entire pipeline and gets automatically called when making a merge request.     |
| `project`            | `processor`              | Runs the build, unit test, integration test and linting stages of the camera processor. |
| `project`            | `orchestrator`           | Runs the build, unit test and linting stages of the processor orchestrator.             |
| `project`            | `interface`              | Runs the build, unit test and linting stages of the interface.                          |
| `project`            | `forwarder`              | Runs the build and linting stages of the video forwarder.                               |
| `stage`              | `build`                  | Runs all build stages of the project.                                                   |
| `stage`              | `test`                   | Runs all test stages of the project.                                                    |
| `stage`              | `lint`                   | Runs all linting stages of the project.                                                 |