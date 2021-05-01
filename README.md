##Running the pipeline:

* Navigate to the Run Pipeline page or <a href="https://git.science.uu.nl/e.w.j.bangma/tracktech/-/pipelines/new" target="_blank">Click Here</a>.
* Select desired branch.
* Input the variables of the desired 

| Input variable key   | Input variable value     | Description									                                            |
|:---------------------|:-------------------------|:----------------------------------------------------------------------------------------|
| `CI_PIPELINE_SOURCE` | `merge_request_event`    | Runs the entire pipeline and gets automatically called when making a merge request.     |
| `PIPELINE`           | `camera_processor`       | Runs the build, unit test, integration test and linting stages of the camera processor. |
| `PIPELINE`           | `processor_orchestrator` | Runs the build, unit test and linting stages of the processor orchestrator.             |
| `PIPELINE`           | `interface`              | Runs the build, unit test and linting stages of the interface.                          |
| `PIPELINE`           | `forwarder`              | Runs the build and linting stages of the video forwarder.                               |
| `PIPELINE`           | `unit_tests`             | Runs all unit-test stages of the project.                                               |
| `PIPELINE`           | `integration_tests`      | Runs all integration test stages of the project.                                        |
| `PIPELINE`           | `linting`                | Runs all linting stages of the project.                                                 |