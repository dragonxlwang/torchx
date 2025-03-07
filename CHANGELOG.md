# CHANGELOG

## torchx-0.1.2

Milestone: https://github.com/pytorch/torchx/milestones/3

* PyTorch 1.11 Support
* Python 3.10 Support
* `torchx.workspace`
  * TorchX now supports a concept of workspaces. This enables seamless launching
    of jobs using changes present in your local workspace. For Docker based
    schedulers, we automatically build a new docker container on job launch
    making it easier than ever to run experiments. #333
* `torchx.schedulers`
  * Ray #329
    * Newly added Ray scheduler makes it easy to launch jobs on Ray.
    * https://pytorch.medium.com/large-scale-distributed-training-with-torchx-and-ray-1d09a329aacb
  * AWS Batch #381
    * Newly added AWS Batch scheduler makes it easy to launch jobs in AWS with minimal infrastructure setup.
  * Slurm
    * Slurm jobs will by default launch in the current working directory to match `local_cwd` and workspace behavior. #372
    * Replicas now have their own log files and can be accessed programmatically. #373
    * Support for `comment`, `mail-user` and `constraint` fields. #391
    * Workspace support (prototype) - Slurm jobs can now be launched in isolated experiment directories. #416
  * Kubernetes
    * Support for running jobs under service accounts. #408
    * Support for specifying instance types. #433
  * All Docker-based Schedulers (Kubernetes, Batch, Docker)
    * Added bind mount and volume supports #420, #426
    * Bug fix: Better shm support for large dataloader #429
    * Support for `.dockerignore` and custom Dockerfiles #401
  * Local Scheduler
    * Automatically set `CUDA_VISIBLE_DEVICES` #383
    * Improved log ordering #366
* `torchx.components`
  * `dist.ddp`
    * Rendezvous works out of the box on all schedulers #400
    * Logs are now prefixed with local ranks #412
    * Can specify resources via the CLI #395
    * Can specify environment variables via the CLI #399
  * HPO
    * Ax runner now lives in the Ax repo https://github.com/facebook/Ax/commit/8e2e68f21155e918996bda0b7d97b5b9ef4e0cba
* `torchx.cli`
  * `.torchxconfig`
    * You can now specify component argument defaults `.torchxconfig` https://github.com/pytorch/torchx/commit/c37cfd7846d5a0cb527dd19c8c95e881858f8f0a
    * `~/.torchxconfig` can now be used to set user level defaults. #378
    * `--workspace` can be configured #397
  * Color change and bug fixes #419
* `torchx.runner`
  * Now supports workspace interfaces. #360
  * Returned lines now preserve whitespace to provide support for progress bars #425
  * Events are now logged to `torch.monitor` when available. #379
* `torchx.notebook` (prototype)
  * Added new workspace interface for developing models and launching jobs via a Jupyter Notebook. #356
* Docs
  * Improvements to clarify TorchX usage w/ workspaces and general cleanups.
  * #374, #402, #404, #407, #434

## torchx-0.1.1

* Milestone: https://github.com/pytorch/torchx/milestone/2

* `torchx.schedulers`
  * #287, #286 - Implement `local_docker` scheduler using docker client lib

* Docs
  * #336 - Add context/intro to each docs page
  * Minor document corrections

* `torchx`
  * #267 - Make torchx.version.TORCHX_IMAGE follow the same semantics as __version__
  * #299 - Use base docker image `pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime`

* `torchx.specs`
  * #301 - Add `metadata` field to `torchx.specs.Role` dataclass
  * #302 - Deprecate RunConfig in favor of raw `Dict[str, ConfigValue]`

* `torchx.cli`
  * #316 - Implement `torchx builtins --print` that prints the source code of the component

* `torchx.runner`
  * #331 - Split run_component into run_component and dryrun_component

## torchx-0.1.0

* `torchx.schedulers`
  * `local_docker` print a nicer error if Docker is not installed #284
* `torchx.cli`
  *  Improved error messages when `-cfg` is not provided #271
* `torchx.components`
  * Update `dist.ddp` to use `c10d` backend as default #263
* `torchx.aws`
  * Removed entirely as it was unused

* Docs
  * Restructure documentation to be more clear
  * Merged Hello World example with the Quickstart guide to reduce confusion
  * Updated Train / Distributed component documentation
  * Renamed configure page to "Advanced Usage" to avoid confusion with experimental .torchxconfig
  * Renamed Localhost page to just Local to better match the class name
  * Misc cleanups / improvements

* Tests
  * Fixed test failure when no secrets are present #274
  * Added macOS variant to our unit tests #209

## torchx-0.1.0rc1

* `torchx.specs`
  * base_image has been deprecated
  * Some predefined AWS specific named_resources have been added
  * Docstrings are no longer required for component definitions to make it
  easier to write them. They will be still rendered as help text if present and
  are encouraged but aren't required.
  * Improved vararg handling logic for components

* `torchx.runner`
  * Username has been removed from the session name
  * Standardized `runopts` naming

* `torchx.cli`
  * Added experimental `.torchxconfig` file which can be used to set default
  scheduler arguments for all runs.
  * Added `--version` flag
  * `builtins` ignores `torchx.components.base` folder

* Docs
  * Improved entry_points and resources docs
  * Better component documentation
  * General improvements and fixes

* Examples
  * Moved examples to be under torchx/ and merged the examples container with
  the primary container to simplify usage.
  * Added a self contained "Hello World" example
  * Switched lightning_classy_vision example to use ResNet model architecture so
  it will actually converage
  * Removed CIFAR example and merged functionality into lightning_classy_vision

* CI
  * Switched to OpenID Connect based auth

## torchx-0.1.0rc0

* `torchx.specs` API release candidate
  (still experimental but no major changes expected for `0.1.0`)
* `torchx.components`
  * made all components use docker images by default for consistency
  * removed binary_component in favor of directly writing app defs
  * `serve.torchserve` - added optional `--port` argument for upload server
  * `utils.copy` - added copy component for easy file transfer between `fsspec` path locations
  * `ddp`
    * `nnodes` no longer needs to be specified and is set from `num_replicas` instead.
    * Bug fixes.
    * End to end integration tests on Slurm and Kubernetes.
  * better unit testing support via `ComponentTestCase`.
* `torchx.schedulers`
  * Split `local` scheduler into `local_docker` and `local_cwd`.
    * For local execution `local_docker` provides the closest experience to remote behavior.
    * `local_cwd` allows reusing the same component definition for local development purposes but resolves entrypoint and deps relative to the current working directory.
  * Improvements/bug fixes to Slurm and Kubernetes schedulers.
* `torchx.pipelines`
  * `kfp` Added the ability to launch distributed apps via the new `resource_from_app` method which creates a Volcano Job from Kubeflow Pipelines.
* `torchx.runner` - general fixes and improvements around wait behavior
* `torchx.cli`
  * Improvements to output formatting to improve clarity.
  * `log` can now log from all roles instead of just one
  * `run` now supports boolean arguments
  * Experimental support for CLI being used from scripts. Exit codes are consistent and only script consumable data is logged on stdout for key commands such as `run`.
  * `--log_level` configuration flag
  * Default scheduler is now `local_docker` and decided by the first scheduler in entrypoints.
  * More robust component finding and better behavior on malformed components.
* `torchx.examples`
   * Distributed CIFAR Training Example
   * HPO
   * Improvements to lightning_classy_vision example -- uses components, datapreproc separated from injection
   * Updated to use same file directory layout as github repo
   * Added documentation on setting up kubernetes cluster for use with TorchX
   * Added distributed KFP pipeline example
* `torchx.runtime`
  * Added experimental `hpo` support with Ax (https://github.com/facebook/Ax)
  * Added experimental `tracking.ResultTracker` for distributed tracking of metrics for use with HPO.
  * Bumped pytorch version to 1.9.0.
  * Deleted deprecated storage/plugins interface.
* Docs
  * Added app/component best practices
  * Added more information on different component archetypes such as training
  * Refactored structure to more accurately represent components, runtime and
    scheduler libraries.
  * README: added information on how to install from source, nightly and different dependencies
  * Added scheduler feature compatibility matrices
  * General cleanups and improvements
* CI
  * component integration test framework
  * codecoverage
  * renamed primary branch to main
  * automated doc push
  * distributed kubernetes integration tests
  * nightly builds at https://pypi.org/project/torchx-nightly/
  * pyre now uses nightly builds
  * added slurm integration tests


## torchx-0.1.0b0

* `torchx.specs` API release candidate
  (still experimental but no major changes expected for `0.1.0`)

* `torchx.pipelines` - Kubeflow Pipeline adapter support
* `torchx.runner` - SLURM and local scheduler support
* `torchx.components` - several utils, ddp, torchserve builtin components
* `torchx.examples`
   * Colab support for examples
   * `apps`:
     * classy vision + lightning trainer
     * torchserve deploy
     * captum model visualization
   * `pipelines`:
     * apps above as a Kubeflow Pipeline
     * basic vs advanced Kubeflow Pipeline examples
* CI
  * unittest, pyre, linter, KFP launch, doc build/test
