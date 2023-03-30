# Define the component configurations
component_configs = {
    'example_gen': 'example_gen = tfx.components.CsvExampleGen(input_base="{input_path}")',
    'statistics_gen': 'statistics_gen = tfx.components.StatisticsGen(examples=example_gen.outputs.examples)',
    'schema_gen': 'schema_gen = tfx.components.SchemaGen(statistics=statistics_gen.outputs.statistics)',
    'example_validator': 'example_validator = tfx.components.ExampleValidator(statistics=statistics_gen.outputs.statistics, schema=schema_gen.outputs.schema)',
    'transform': 'transform = tfx.components.Transform(examples=example_gen.outputs.examples, schema=schema_gen.outputs.schema, module_file="{module_path}")',
    'trainer': 'trainer = tfx.components.Trainer(
        module_file="{module_path}",
        transformed_examples=transform.outputs.transformed_examples,
        schema=schema_gen.outputs.schema,
        transform_graph=transform.outputs.transform_graph,
        train_args=tfx.proto.TrainArgs(num_steps=1000),
        eval_args=tfx.proto.EvalArgs(num_steps=500)
    )',
    'evaluator': 'evaluator = tfx.components.Evaluator(examples=example_gen.outputs.examples, model=trainer.outputs.model, schema=schema_gen.outputs.schema)',
    'pusher': 'pusher = tfx.components.Pusher(model_export=trainer.outputs.model, serving_model_dir="{serving_path}")'
}

# Define the pipeline configuration
pipeline_config = {
    'pipeline_name': 'my_pipeline',
    'pipeline_root': '/path/to/pipeline_root',
    'components': []
}

# Generate the component code and add to the pipeline configuration
for component_name in user_selected_components:
    component_config = component_configs[component_name]
    pipeline_config['components'].append(component_config)

# Generate the pipeline code dynamically
pipeline_code = '''
pipeline = tfx.dsl.Pipeline(
    pipeline_name='{pipeline_name}',
    pipeline_root='{pipeline_root}',
    components=[
        {component_code}
    ]
)
'''.format(
    pipeline_name=pipeline_config['pipeline_name'],
    pipeline_root=pipeline_config['pipeline_root'],
    component_code=',\n'.join(pipeline_config['components'])
)

# Print the pipeline code
print(pipeline_code)