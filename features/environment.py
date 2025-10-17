# Note on environment.py
#
# While the core steps live in features/steps/, you should use features/environment.py to define hooks like before_all, after_all, before_scenario, and after_scenario. This is the perfect place to:
#
#     Create the root temporary directory before the entire test run starts.
#
#     Define context variables (like context.source_path and context.dest_path) and automatically pass them to your step definitions.
#
#     Clean up all temporary directories after the tests are done. This ensures full isolation and cleanup.
