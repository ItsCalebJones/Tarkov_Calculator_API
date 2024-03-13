import argparse

import uvicorn

from tarkov_calculator_api.gunicorn_runner import GunicornApplication
from tarkov_calculator_api.services.scheduler import TarkovItemScheduler
from tarkov_calculator_api.settings import settings

parser = argparse.ArgumentParser(description="Tarkov Market Calculator")
parser.add_argument(
    "--service",
    action="store_true",
    help="Run the Tarkov Item Scheduler service.",
)
parser.add_argument(
    "--api",
    action="store_true",
    help="Run the Tarkov Market Calculator API.",
)
parser.set_defaults(service=False)
parser.set_defaults(api=False)
args = parser.parse_args()

# Use args.option1 and args.option2 in your code as needed


def main() -> None:
    """Entrypoint of the application."""
    if args.api is False and args.service is False:
        print("Please specify --api or --service... Exiting.")
    if args.service:
        TarkovItemScheduler().run()
    elif args.api is True:
        if settings.reload:
            uvicorn.run(
                "tarkov_calculator_api.web.application:get_app",
                workers=settings.workers_count,
                host=settings.host,
                port=settings.port,
                reload=settings.reload,
                log_level=settings.log_level.value.lower(),
                factory=True,
            )
        else:
            # We choose gunicorn only if reload
            # option is not used, because reload
            # feature doen't work with Uvicorn workers.
            GunicornApplication(
                "tarkov_calculator_api.web.application:get_app",
                host=settings.host,
                port=settings.port,
                workers=settings.workers_count,
                factory=True,
                accesslog="-",
                loglevel=settings.log_level.value.lower(),
                access_log_format='%r "-" %s "-" %Tf',  # noqa: WPS323
            ).run()


if __name__ == "__main__":
    main()
