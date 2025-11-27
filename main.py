"""
Main entry point for the ELT system
"""
import logging
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.core import ConfigManager, setup_logger
from src.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


def run_once(config_path: str = "config/config.yaml"):
    """
    Run all pipelines once
    
    Args:
        config_path: Path to configuration file
    """
    # Load configuration
    config_manager = ConfigManager(config_path)
    
    # Setup logging
    log_config = config_manager.get_logging_config()
    setup_logger(log_config)
    
    logger.info("=" * 60)
    logger.info("ELT System - Single Run")
    logger.info("=" * 60)
    
    # Create and run orchestrator
    orchestrator = Orchestrator(config_manager)
    results = orchestrator.run_all()
    
    return results


def run_scheduled(config_path: str = "config/config.yaml"):
    """
    Run pipelines on a schedule
    
    Args:
        config_path: Path to configuration file
    """
    # Load configuration
    config_manager = ConfigManager(config_path)
    
    # Setup logging
    log_config = config_manager.get_logging_config()
    setup_logger(log_config)
    
    logger.info("=" * 60)
    logger.info("ELT System - Scheduled Mode")
    logger.info("=" * 60)
    
    # Create orchestrator
    orchestrator = Orchestrator(config_manager)
    
    # Setup scheduler
    scheduler = BlockingScheduler()
    
    # Add jobs for each source with its configured interval
    for source_config in config_manager.get_enabled_sources():
        source_name = source_config.get('name')
        interval_minutes = source_config.get('sync', {}).get('interval_minutes', 60)
        
        scheduler.add_job(
            lambda name=source_name: orchestrator.run_source(name),
            trigger=IntervalTrigger(minutes=interval_minutes),
            id=f"pipeline_{source_name}",
            name=f"Pipeline: {source_name}",
            replace_existing=True
        )
        
        logger.info(f"Scheduled pipeline '{source_name}' to run every {interval_minutes} minutes")
    
    # Run all pipelines immediately on startup
    logger.info("Running initial sync...")
    orchestrator.run_all()
    
    # Start scheduler
    logger.info("Scheduler started. Press Ctrl+C to exit.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="ELT System - Extract, Load, Transform")
    parser.add_argument(
        '--mode',
        choices=['once', 'scheduled'],
        default='once',
        help='Run mode: once (single run) or scheduled (continuous)'
    )
    parser.add_argument(
        '--config',
        default='config/config.yaml',
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'once':
            run_once(args.config)
        else:
            run_scheduled(args.config)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
