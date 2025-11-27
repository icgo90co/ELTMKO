"""
ELT Pipeline Orchestrator
Coordinates extraction, loading, and transformation operations
"""
import logging
from typing import Dict, Any, List
from datetime import datetime
import pandas as pd

from src.core import ConfigManager
from src.extractors import FacebookAdsExtractor
from src.loaders import MySQLLoader

logger = logging.getLogger(__name__)


class Pipeline:
    """Orchestrates the ELT pipeline for a single source-destination pair"""
    
    def __init__(self, source_config: Dict[str, Any], destination_config: Dict[str, Any]):
        """
        Initialize pipeline
        
        Args:
            source_config: Source configuration
            destination_config: Destination configuration
        """
        self.source_config = source_config
        self.destination_config = destination_config
        self.source_name = source_config.get('name')
        self.source_type = source_config.get('type')
        self.destination_name = destination_config.get('name')
        
        # Initialize extractor based on source type
        self.extractor = self._create_extractor()
        
        # Initialize loader based on destination type
        self.loader = self._create_loader()
    
    def _create_extractor(self):
        """Create appropriate extractor based on source type"""
        if self.source_type == 'facebook_ads':
            return FacebookAdsExtractor(self.source_config.get('config', {}))
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")
    
    def _create_loader(self):
        """Create appropriate loader based on destination type"""
        dest_type = self.destination_config.get('type')
        
        if dest_type == 'mysql':
            return MySQLLoader(self.destination_config.get('config', {}))
        else:
            raise ValueError(f"Unsupported destination type: {dest_type}")
    
    def run(self):
        """Execute the ELT pipeline"""
        logger.info(f"Starting ELT pipeline: {self.source_name} -> {self.destination_name}")
        
        start_time = datetime.now()
        total_rows = 0
        
        try:
            # Connect to destination
            self.loader.connect()
            
            # Get tables to sync from configuration
            tables = self.source_config.get('sync', {}).get('tables', [])
            
            for table_config in tables:
                table_name = table_config.get('name')
                
                try:
                    logger.info(f"Processing table: {table_name}")
                    
                    # Extract data
                    df = self.extractor.extract_table(table_config)
                    
                    if df.empty:
                        logger.warning(f"No data extracted for table '{table_name}'")
                        continue
                    
                    # Load data
                    target_table = f"{self.source_type}_{table_name}"
                    
                    # Use upsert for tables with IDs, otherwise append
                    if 'id' in df.columns:
                        self.loader.upsert_dataframe(df, target_table, key_columns=['id'])
                    else:
                        self.loader.load_dataframe(df, target_table, mode='append')
                    
                    total_rows += len(df)
                    
                except Exception as e:
                    logger.error(f"Error processing table '{table_name}': {e}")
                    continue
            
            # Disconnect from destination
            self.loader.disconnect()
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Pipeline completed successfully in {duration:.2f}s. Total rows: {total_rows}")
            
            return {
                'success': True,
                'rows': total_rows,
                'duration': duration
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            
            # Ensure loader is disconnected
            try:
                self.loader.disconnect()
            except:
                pass
            
            return {
                'success': False,
                'error': str(e)
            }


class Orchestrator:
    """Manages and executes multiple ELT pipelines"""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize orchestrator
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.pipelines: List[Pipeline] = []
        self._create_pipelines()
    
    def _create_pipelines(self):
        """Create pipelines from configuration"""
        sources = self.config_manager.get_enabled_sources()
        
        for source in sources:
            destination_name = source.get('destination')
            
            try:
                destination = self.config_manager.get_destination(destination_name)
                
                if not destination.get('enabled', False):
                    logger.warning(f"Destination '{destination_name}' is disabled, skipping source '{source.get('name')}'")
                    continue
                
                pipeline = Pipeline(source, destination)
                self.pipelines.append(pipeline)
                
                logger.info(f"Created pipeline: {source.get('name')} -> {destination_name}")
                
            except ValueError as e:
                logger.error(f"Error creating pipeline for source '{source.get('name')}': {e}")
                continue
    
    def run_all(self):
        """Execute all configured pipelines"""
        logger.info(f"Running {len(self.pipelines)} pipeline(s)...")
        
        results = []
        
        for pipeline in self.pipelines:
            result = pipeline.run()
            results.append({
                'source': pipeline.source_name,
                'destination': pipeline.destination_name,
                **result
            })
        
        # Summary
        successful = sum(1 for r in results if r.get('success'))
        failed = len(results) - successful
        total_rows = sum(r.get('rows', 0) for r in results if r.get('success'))
        
        logger.info(f"All pipelines completed. Success: {successful}, Failed: {failed}, Total rows: {total_rows}")
        
        return results
    
    def run_source(self, source_name: str):
        """
        Execute pipeline for a specific source
        
        Args:
            source_name: Name of the source to run
        """
        pipeline = next((p for p in self.pipelines if p.source_name == source_name), None)
        
        if pipeline is None:
            raise ValueError(f"Pipeline not found for source: {source_name}")
        
        return pipeline.run()
