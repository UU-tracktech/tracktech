Hieronder staat een tabel met alle manieren om de CI pipeline te runnen.
________________________________________________________________________________________________________________________________________
|                    |                        |                                                                                        |
|Input variable key  | Input variable value   | Description									       |
|______________________________________________________________________________________________________________________________________|
|		     |			      |	  										       |
|CI_PIPELINE_SOURCE  | merge_request_event    | Runs the entire pipeline and gets automatically called when making a merge request     |
|______________________________________________________________________________________________________________________________________|
|		     |			      |											       |
|PIPELINE            | camera_processor       | Runs the build, unit test, integration test and linting stages of the camera processor |
|______________________________________________________________________________________________________________________________________|
|		     |			      |											       |
|PIPELINE            | processor_orchestrator | Runs the build, unit test and linting stages of the processor orchestrator             |
|______________________________________________________________________________________________________________________________________|
|		     |			      |											       |
|PIPELINE            | interface              | Runs the build, unit test and linting stages of the interface                          |
|______________________________________________________________________________________________________________________________________|
|		     |			      |											       |
|PIPELINE            | forwarder              | Runs the build and linting stages of the video forwarder                               |
|______________________________________________________________________________________________________________________________________|
|		     |			      |											       |
|PIPELINE            | unit_tests             | Runs all unit_test stages of the project                                               |
|______________________________________________________________________________________________________________________________________|
|		     |			      |											       |
|PIPELINE            | integration_tests      | Runs all integration test stages of the project                                        |
|______________________________________________________________________________________________________________________________________|
|		     |			      |											       |
|PIPELINE            | linting                | Runs all linting stages of the project                                                 |
|______________________________________________________________________________________________________________________________________|
