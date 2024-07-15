import os
import click
import logging
from tqdm import tqdm
import time
from mg_miner.core.file_collector import FileCollector
from mg_miner.core.component_detector import ComponentDetector
from mg_miner.core.redactor import Redactor
from mg_miner.core.summary_creator import SummaryCreator
from mg_miner.utils.utils import setup_logging, load_config, get_trace_id

@click.group()
@click.option('--config', default='configs/config.yaml', help='Path to the configuration file.')
@click.option('--verbose', is_flag=True, help='Enable verbose output.')
@click.pass_context
def cli(ctx, config, verbose):
    """Main CLI entry point."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose
    ctx.obj['trace_id'] = get_trace_id()
    setup_logging(config, verbose)

@cli.command()
@click.pass_context
def collect(ctx):
    """Collect files based on configuration."""
    try:
        config = load_config(ctx.obj['config'])
        file_collector = FileCollector.from_config(config)
        logging.info(f"Trace ID: {ctx.obj['trace_id']} - Collecting files...")
        file_collector.collect_files()
    except Exception as e:
        logging.error(f"Error in collect command: {e}")

@cli.command()
@click.pass_context
def detect(ctx):
    """Detect components based on collected files."""
    try:
        config = load_config(ctx.obj['config'])
        component_detector = ComponentDetector(output_dir=config['output_dir'], silent=False)
        logging.info(f"Trace ID: {ctx.obj['trace_id']} - Detecting components...")
        component_detector.detect_components()
    except Exception as e:
        logging.error(f"Error in detect command: {e}")

@cli.command()
@click.pass_context
def redact(ctx):
    """Redact sensitive information based on compliance standards."""
    try:
        config = load_config(ctx.obj['config'])
        redactor = Redactor(output_dir=config['output_dir'], compliance_standards=['GDPR', 'HIPAA'])
        logging.info(f"Trace ID: {ctx.obj['trace_id']} - Redacting sensitive information...")
        redactor.redact_sensitive_info()
    except Exception as e:
        logging.error(f"Error in redact command: {e}")

@cli.command()
@click.pass_context
def summary(ctx):
    """Create a summary of the project."""
    try:
        config = load_config(ctx.obj['config'])
        summary_creator = SummaryCreator(output_dir=config['output_dir'], theme='default', silent=False)
        logging.info(f"Trace ID: {ctx.obj['trace_id']} - Creating summary...")
        summary_creator.create_summary()
    except Exception as e:
        logging.error(f"Error in summary command: {e}")

@cli.command()
@click.pass_context
@click.option('--tasks', default=100, help='Number of tasks to complete.')
def run_tasks(ctx, tasks):
    """Run tasks with progress bar, ETA, and post-run analysis."""
    try:
        setup_logging(ctx.obj['config'], ctx.obj['verbose'])
        task_times = []

        for _ in tqdm(range(tasks), desc="Processing", unit="task"):
            start_time = time.time()
            time.sleep(0.1)  # Simulate a task taking time
            end_time = time.time()
            task_times.append(end_time - start_time)
        
        analyze_run(task_times)
    except Exception as e:
        logging.error(f"Error in run_tasks command: {e}")

def analyze_run(task_times):
    """Analyze the run and provide suggestions."""
    try:
        total_time = sum(task_times)
        avg_time = total_time / len(task_times)
        
        logging.info(f"Total Time: {total_time:.2f} seconds")
        logging.info(f"Average Time per Task: {avg_time:.2f} seconds")
        
        if avg_time > 0.1:
            logging.warning("Suggestion: Consider optimizing the task execution time.")
        else:
            logging.info("Great job! The tasks are executing efficiently.")
    except Exception as e:
        logging.error(f"Error in analyze_run: {e}")

if __name__ == '__main__':
    cli()
